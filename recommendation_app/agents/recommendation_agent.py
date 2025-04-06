import ollama
import time
from datetime import datetime
from .product_agent import ProductAgent
from ..models import Customer

class RecommendationAgent:
    def __init__(self, customer_id, batch_size=20):
        self.customer_id = customer_id
        self.customer = Customer.objects.get(customer_id=customer_id)
        self.product_agent = ProductAgent(customer_id)
        self.filtered_products = self.product_agent.get_filtered_products()
        self.customer_analysis = self.product_agent.customer_analysis
        self.batch_size = batch_size

    def _get_current_season(self):
        month = datetime.now().month
        return (
            "Spring" if 3 <= month <= 5 else
            "Summer" if 6 <= month <= 8 else
            "Autumn" if 9 <= month <= 11 else
            "Winter"
        )

    def _chunk_products(self):
        print(f"📦 Total products: {len(self.filtered_products)}")
        for i in range(0, len(self.filtered_products), self.batch_size):
            yield self.filtered_products[i:i + self.batch_size]

    def _ask_llm_for_batch(self, product_batch, batch_num, batch_recs=5, retries=3):
        product_list_text = "\n".join(
            f"- Product ID: {p['product_id']}, "
            f"Category: {p['category']}/{p['subcategory']}, "
            f"Brand: {p['brand']}, "
            f"Price: ${p['price']}, "
            f"Rating: {p['product_rating']}, "
            f"Sentiment: {p['review_sentiment_score']}, "
            f"Holiday: {'Yes' if p['holiday'] else 'No'}, "
            f"Season: {p['season']}, "
            f"Geo: {p['geographical_location']}, "
            f"Prob. of Recommendation: {p['probability_of_recommendation']}"
            for p in product_batch
        )

        prompt = f"""
        You are a smart product recommendation assistant.

        This is batch #{batch_num} of relevant products. Pick the top {batch_recs} that best match the customer below based on:
        - If there are more than one category then please keep the recommendation for that category also this is mandatory.
        - Purchase and browsing history
        - Current season
        - Holiday relevance
        - Ratings, sentiment, and recommendation probability

        ### Customer Info
        - Age: {self.customer.age}
        - Gender: {self.customer.gender}
        - Location: {self.customer.location}
        - Browsing History: {self.customer.browsing_history or 'None'}
        - Purchase History: {self.customer.purchase_history or 'None'}
        - Segment: {self.customer.customer_segment}
        - Avg Order Value: {self.customer.avg_order_value}
        - Holiday Shopper: {'Yes' if self.customer.holiday else 'No'}
        - Favorite Season: {self.customer.season}
        - Current Season: {self._get_current_season()}

        ### Customer Insights
        {self.customer_analysis}

        ### Product Batch
        {product_list_text}

        ### Response Format
        - 1. Product ID: P12345
        - 2. Product ID: P67890
        + Pick ONLY from the products listed above. Do NOT invent or guess product.
        + Do NOT include any other text or explanation.
        + Do NOT include any process or method.
        + Do NOT include any product that is not in the list above or below in the response format and also dont print prompt strictly.
        + Respond only in the form of product IDs only.
        """

        for attempt in range(retries):
            try:
                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['message']['content'].strip()
            except Exception as e:
                print(f"⚠️ Batch {batch_num} attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        return f"⚠️ AI failed to respond for batch #{batch_num}."

    def get_recommendations(self):
        if not self.filtered_products:
            return "No relevant products found."

        all_recommendations = []

        for batch_num, product_batch in enumerate(self._chunk_products(), start=1):
            if batch_num > 3:
                break
            print(f"📦 Processing batch #{batch_num} with {len(product_batch)} products...")
            result = self._ask_llm_for_batch(product_batch, batch_num)
            all_recommendations.append(result)

        combined = "\n".join(all_recommendations)
        return combined.split("\n")

