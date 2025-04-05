from django.shortcuts import render, HttpResponse
from .models import Customer
from .agents.customer_agent import *
from .agents.product_agent import *

def home(request):
    customers = Customer.objects.all()
    customers = customers[:10]
    return render(request, 'home.html', {'customers': customers})

def get_list_products(request, customer_id):
    customer_analysis = run_customer_analysis(customer_id)
    product_agent = ProductAgent(customer_id)
    filtered_products = product_agent.get_filtered_products()
    context = {
        'customer_analysis': customer_analysis,
        'filtered_products': filtered_products,
    }
    return render(request, 'home.html', context)
