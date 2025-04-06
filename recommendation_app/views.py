from django.shortcuts import render, HttpResponse
from .models import Customer
from .agents.customer_agent import *
from .agents.product_agent import *
from .agents.recommendation_agent import *

def home(request):
    customers = Customer.objects.all()
    customers = customers[:10]
    return render(request, 'home.html', {'customers': customers})

def get_list_products(request, customer_id):
    customer_analysis = run_customer_analysis(customer_id)

    product_agent = ProductAgent(customer_id)
    filtered_products = product_agent.get_filtered_products()

    agent = RecommendationAgent(customer_id)
    recommendation_ids = agent.get_recommendations()

    recommended_products = Product.objects.filter(product_id__in=recommendation_ids)

    context = {
        'customer_analysis': customer_analysis,
        'filtered_products': filtered_products,
        'recommended_products': recommended_products,
    }

    return render(request, 'home.html', context)
