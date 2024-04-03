from django.shortcuts import render
from product_management.models import Product

product_management_temp = "product_management/templates"
product_management_static = "product_management/static"

def index(request):
    product_data = Product.objects.all()
    print("-----------------product_data",product_data)
    return render(request, f"{product_management_temp}/index.html",{"product_info":product_data})