from django.shortcuts import render, HttpResponse
from .models import Customer
from .agents.customer_agent import *

def home(request):
    customers = Customer.objects.all()
    customers = customers[:10]
    return render(request, 'home.html', {'customers': customers})
