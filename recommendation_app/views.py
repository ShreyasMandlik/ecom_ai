from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .agents.customer_agent import CustomerAgent, run_customer_analysis
from .agents.recommendation_agent import RecommendationAgent
from django.forms.models import model_to_dict


def customer_dashboard(request, customer_id):
    agent = CustomerAgent(customer_id)
    customer = agent.get_customer()
    return render(request, 'home.html', {'customer': customer})

def api_customer_analysis(request,customer_id):
    customer_analysis = run_customer_analysis(customer_id)
    return JsonResponse({'analysis': customer_analysis})

def api_recommended_products(request, customer_id):
    agent = RecommendationAgent(customer_id)
    recommendation_ids = agent.get_recommendations()
    products = Product.objects.filter(product_id__in=recommendation_ids)
    product_list = [model_to_dict(product) for product in products]

    return JsonResponse({'products': product_list})
