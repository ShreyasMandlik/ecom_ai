from recommendation_app.models import Customer
import ollama
import re
import time

from recommendation_app.models import Customer
import ollama
import json
import re
import time

class CustomerAgent:
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)

    def get_customer_analysis(self, retries=5):
        """Dynamically generate customer behavior analysis using AI."""
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

        ### **Response Format (STRICTLY FOLLOW)**
        Respond **only** in this format:
        ```
        "Analysis": "<2-3 sentence summary explaining why this customer is in this segment and what category they are more likely to engage with>"
        ```
        """

        for attempt in range(retries):
            try:
                response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
                raw_content = response['message']['content'].strip()

                match = re.search(r'"Analysis":\s*"([^"]+)"', raw_content)
                extracted_text = match.group(1) if match else raw_content

                if extracted_text and not extracted_text.startswith("<") and "explaining why this customer is" not in extracted_text:
                    print("Extracted text:", extracted_text)
                    return extracted_text
                print(f"⚠️ Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Error on attempt {attempt + 1}: {e}. Retrying...")
                time.sleep(2)

        return "⚠️ AI failed to generate a valid response after multiple attempts."


def run_customer_analysis(customer_id):
    agent = CustomerAgent(customer_id)
    return agent.get_customer_analysis()
