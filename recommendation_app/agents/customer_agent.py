from recommendation_app.models import Customer
import ollama
import json
import re
import time

class CustomerAgent:
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)

    def get_customer_analysis(self, retries=5):
        prompt = f"""
        You are an AI specializing in customer behavior analysis for an e-commerce platform.
        Analyze the given customer data and provide a **brief** explanation for why they belong to the **{self.customer.customer_segment}** category.
        Then, determine what product category they are most likely to engage with.

        ---

        ### **Customer Data:**
        - Age: {self.customer.age}
        - Gender: {self.customer.gender}
        - Location: {self.customer.location}
        - Browsing History: {self.customer.browsing_history}
        - Purchase History: {self.customer.purchase_history}
        - Average Order Value: {self.customer.avg_order_value}
        - Holiday Shopper: {'Yes' if self.customer.holiday else 'No'}
        - Favorite Season: {self.customer.season}
        - **Segment (Predefined):** {self.customer.customer_segment}

        ---

        ### ** Response Format (STRICTLY FOLLOW)**
        - Respond ONLY in the following JSON format:
        ```json
        {{
            "Analysis": "<2-3 sentence summary explaining why this customer is in this segment and what category they are more likely to engage with>"
        }}
        ```
        - Do **NOT** return placeholder text.
        - Do **NOT** repeat the prompt.
        - Do **NOT** return explanations or markdown.

        If you are unsure, respond with:
        ```json
        {{
            "Analysis": "Unable to generate a meaningful response."
        }}
        ```
        """

        for attempt in range(retries):
            try:
                response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
                raw_content = response['message']['content']
                analysis = json.loads(raw_content)
                if analysis["Analysis"].startswith("<") or "explaining why this customer is" in analysis["Analysis"]:
                    print(f"⚠️ Attempt {attempt + 1} returned invalid response. Retrying...")
                    time.sleep(2)
                    continue
                self.customer.llm_analysis = json.dumps(analysis)
                self.customer.save()
                return self.customer

            except (json.JSONDecodeError, KeyError):
                match = re.search(r'"Analysis":\s*"([^"]+)"', raw_content)
                extracted_text = match.group(1) if match else None

                if extracted_text and not extracted_text.startswith("<"):
                    analysis = {"Analysis": extracted_text}
                    self.customer.llm_analysis = json.dumps(analysis)
                    self.customer.save()
                    return self.customer
                else:
                    print(f"⚠️ Attempt {attempt + 1} failed. Retrying...")
                    time.sleep(2)

        self.customer.llm_analysis = json.dumps({"Analysis": "⚠️ AI failed to generate a valid response after multiple attempts."})
        self.customer.save()
        return self.customer

def run_customer_analysis(customer_id):
    agent = CustomerAgent(customer_id)
    return agent.get_customer_analysis()
