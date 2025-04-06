from django.shortcuts import render, HttpResponse
from .models import Customer
from .agents.customer_agent import *
from .agents.product_agent import *
from .agents.recommendation_agent import *


def customer_home(request, customer_id):
    customerAgent = CustomerAgent(customer_id)
    customer = customerAgent.get_customer()
    print('customer',customer.age)
    customer_analysis = run_customer_analysis(customer_id)
    context = {
        'customer': customer,
        'customer_analysis': customer_analysis
    }
    return render(request, 'home.html', context)

def get_recommended_products(request, customer_id):
    print(f"[DEBUG] Fetching recommendations for Customer ID: {customer_id}")
    agent = RecommendationAgent(customer_id)
    recommendation_ids = agent.get_recommendations()
    recommended_products = Product.objects.filter(product_id__in=recommendation_ids)
    context = {
        'recommended_products': recommended_products,
    }
    return render(request, 'recommendations.html', context)
