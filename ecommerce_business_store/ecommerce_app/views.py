from django.shortcuts import render
from django.http import HttpResponse
from ecommerce_app.models import Customer

def index(request):
    emp_all_details = Customer.objects.all()
    return render(request,"ecommerce_app/index.html",context={"emp_details":emp_all_details})