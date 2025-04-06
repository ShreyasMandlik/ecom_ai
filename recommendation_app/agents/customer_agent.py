from recommendation_app.models import Customer
import ollama
import re
import time


class CustomerAgent:
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)

    def get_customer(self):
        return self.customer

    def get_customer_analysis(self, retries=5, delay=2):
        """Generate a clean customer behavior analysis using LLM."""

        prompt = f"""
        You are an AI analyst for an e-commerce platform.

        Based on the customer data below, briefly explain why this customer belongs to the "{self.customer.customer_segment}" segment, and what product categories they are most likely to be interested in.

        Customer:
        - Age: {self.customer.age}
        - Gender: {self.customer.gender}
        - Location: {self.customer.location}
        - Browsing History: {self.customer.browsing_history}
        - Purchase History: {self.customer.purchase_history}
        - Avg Order Value: {self.customer.avg_order_value}
        - Holiday Shopper: {"Yes" if self.customer.holiday else "No"}
        - Favorite Season: {self.customer.season}
        - Segment: {self.customer.customer_segment}

        Respond in 2–3 sentences only.
        """

        for attempt in range(1, retries + 1):
            try:
                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[{"role": "user", "content": prompt}]
                )
                raw_content = response['message']['content'].strip()

                match = re.search(r'"Analysis":\s*"([^"]+)"', raw_content)
                if match:
                    return match.group(1)

                if "Analysis" not in raw_content:
                    return raw_content

                print(f"Attempt {attempt} failed to extract analysis. Retrying...")
            except Exception as e:
                print(f"Error on attempt {attempt}: {e}")
            time.sleep(delay)

        return "⚠️ AI failed to generate a valid analysis after multiple attempts."


def run_customer_analysis(customer_id):
    agent = CustomerAgent(customer_id)
    result = agent.get_customer_analysis()
    return result
