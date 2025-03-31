from django.shortcuts import render
from .models import Customer
from .agents.customer_agent import *

def home(request):
    customers = Customer.objects.all()
    customers = customers[:10 ]
    return render(request, 'home.html', {'customers': customers})


def get_customer(request, customer_id):
    customer = run_customer_analysis(customer_id)
    return render(request, 'customer.html', {'customer': customer})
