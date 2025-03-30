import os
import sys
import django
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_ai.settings")
django.setup()

from recommendation_app.models import Product, Customer

csv_file_path = "/home/shreyas/Desktop/data science/Project/ecom_ai/ecommerce_ai/recommendation_app/data/customer_data_collection.csv"
csv_file_path2 = "/home/shreyas/Desktop/data science/Project/ecom_ai/ecommerce_ai/recommendation_app/data/product_recommendation_data.csv"

df = pd.read_csv(csv_file_path)
df1 = pd.read_csv(csv_file_path2)

customers = [
    Customer(
        customer_id=row['Customer_ID'],
        age=row['Age'],
        gender=row['Gender'],
        location=row['Location'],
        browsing_history=row['Browsing_History'],
        purchase_history=row['Purchase_History'],
        customer_segment=row['Customer_Segment'],
        avg_order_value=row['Avg_Order_Value'],
        holiday=str(row['Holiday']).strip().lower() == "yes",
        season=row['Season']
    )
    for _, row in df.iterrows()
]
Customer.objects.bulk_create(customers)

products = [
    Product(
        product_id=row['Product_ID'],
        category=row['Category'],
        subcategory=row['Subcategory'],
        price=row['Price'],
        brand=row['Brand'],
        avg_rating_similar_products=row['Average_Rating_of_Similar_Products'],
        product_rating=row['Product_Rating'],
        review_sentiment_score=row['Customer_Review_Sentiment_Score'],
        holiday=str(row['Holiday']).strip().lower() == "yes",
        season=row['Season'],
        geographical_location=row['Geographical_Location'],
        similar_product_list=row['Similar_Product_List'],
        probability_of_recommendation=row['Probability_of_Recommendation']
    )
    for _, row in df1.iterrows()
]
Product.objects.bulk_create(products)

print("✅ CSV data imported successfully!")
