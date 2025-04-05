import ollama
from .customer_agent import run_customer_analysis
from ..models import Customer, Product
import pandas as pd
import re

class ProductAgent:
    flattened_products = []
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)
        self.customer_analysis = run_customer_analysis(customer_id)
        self.products = Product.objects.all()


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

    def get_filtered_products(self):
        customer_analysis = self.customer_analysis.lower()
        print("Customer Analysis:", customer_analysis)
        unique_categories = self.extract_categories_from_analysis(customer_analysis)
        print("Matched Categories:", unique_categories)
        products_df = pd.DataFrame(list(self.products.values()))
        for category in unique_categories:
            filtered_category_products = products_df[products_df['category'].str.lower() == category.lower()]
            self.flattened_products.extend(filtered_category_products.to_dict('records'))

        return self.flattened_products
