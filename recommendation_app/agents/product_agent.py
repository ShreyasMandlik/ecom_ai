from .customer_agent import run_customer_analysis
from ..models import Customer, Product
import pandas as pd
import re
import random
import datetime


class ProductAgent:
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)
        self.customer_analysis = run_customer_analysis(customer_id)
        self.products = Product.objects.all()
        self.flattened_products = []

    def get_unique_category(self):
        products_df = pd.DataFrame(list(self.products.values()))
        products_df['category'] = products_df['category'].str.lower()
        unique_categories = products_df['category'].unique()
        return unique_categories

    def extract_categories_from_analysis(self, analysis_text):
        category_keywords = self.get_unique_category()
        analysis_text = str(analysis_text).lower()
        matched_categories = []

        for category in category_keywords:
            if re.search(r'\b' + re.escape(category) + r'\b', analysis_text):
                matched_categories.append(category)

        return list(set(matched_categories))

    def score_product(self, product: dict) -> float:
        """
        Composite score using available fields in Product model, including price affinity.
        """
        prob = product.get("probability_of_recommendation", 0.0)
        rating = product.get("product_rating", 0.0)
        avg_similar = product.get("avg_rating_similar_products", 0.0)
        sentiment = product.get("review_sentiment_score", 0.0)
        holiday = product.get("holiday", False)
        product_season = product.get("season", "").lower()
        product_price = product.get("price", 0.0)
        customer_avg_order = self.customer.avg_order_value or 0.0

        # Determine current season
        month = datetime.datetime.now().month
        if month in [3, 4, 5]:
            current_season = "spring"
        elif month in [6, 7, 8]:
            current_season = "summer"
        elif month in [9, 10, 11]:
            current_season = "autumn"
        else:
            current_season = "winter"

        if customer_avg_order > 0:
            price_score = max(0.0, 1.0 - abs(product_price - customer_avg_order) / customer_avg_order)
        else:
            price_score = 0.5

        score = (
            0.50 * prob +
            0.10 * price_score +
            0.10 * avg_similar +
            0.15 * sentiment +
            0.14 * rating +
            (0.025 if holiday else 0.0) +
            (0.025 if product_season == current_season else 0.0)
        )

        return score

    def get_filtered_products(self):
        customer_analysis = self.customer_analysis.lower()
        unique_categories = self.extract_categories_from_analysis(customer_analysis)

        products_df = pd.DataFrame(list(self.products.values()))
        self.flattened_products = []

        for category in unique_categories:
            filtered_category_products = products_df[
                products_df['category'].str.lower() == category.lower()
            ]
            print(f"📂 {category}: {len(filtered_category_products)} products")
            self.flattened_products.extend(filtered_category_products.to_dict('records'))

        print(f"Total filtered products: {len(self.flattened_products)}")

        random.shuffle(self.flattened_products)
        for product in self.flattened_products:
            product["score"] = self.score_product(product)

        sorted_products = sorted(self.flattened_products, key=lambda x: x["score"], reverse=True)
        top_100_products = sorted_products[:100]

        print(f"⚡ Top 100 products selected")
        return top_100_products
