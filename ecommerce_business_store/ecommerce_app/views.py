from django.shortcuts import render
from django.http import HttpResponse
from ecommerce_app.models import Customer
from ecommerce_app.forms import CustomerInfo

def index(request):
    emp_all_details = Customer.objects.all()
    return render(request,"ecommerce_app/index.html",context={"emp_details":emp_all_details})

def customer_register(request):
    form = CustomerInfo()
    print("--------------",dict(request.session))
    return render(request,'ecommerce_app/index.html',context={"cust_register":form})