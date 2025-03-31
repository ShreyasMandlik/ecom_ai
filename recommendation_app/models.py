from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    browsing_history = models.TextField(blank=True, null=True)
    purchase_history = models.TextField(blank=True, null=True)
    customer_segment = models.CharField(max_length=50, blank=True, null=True)
    avg_order_value = models.FloatField(blank=True, null=True)
    holiday = models.BooleanField(default=False)
    season = models.CharField(max_length=20, blank=True, null=True)
    llm_analysis = models.TextField(blank=True)

    def __str__(self):
        return f"Customer {self.customer_id or 'Unknown'}"

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    avg_rating_similar_products = models.FloatField()
    product_rating = models.FloatField()
    review_sentiment_score = models.FloatField()
    holiday = models.BooleanField()
    season = models.CharField(max_length=20)
    geographical_location = models.CharField(max_length=100)
    similar_product_list = models.JSONField()
    probability_of_recommendation = models.FloatField()

    def __str__(self):
        return self.product_id
