from django.shortcuts import render
from product_management.models import *
from django.contrib.auth.models import User

product_management_temp = "product_management/templates"
product_management_static = "product_management/static"


def index(request):
    product_data = Product.objects.all()
    print("-----------------product_data",product_data)
    return render(request, f"{product_management_temp}/index.html",{"product_info":product_data})

def saves():
    car = Car(title = "check",price=200)
    car.save()  
    print("-----------------before refreshing from db")
    car.refresh_from_db()
    car.arefresh_from_db()

def gets():
    car = Car.objects.defer("price").first()
    print("-----------------car--first>",car)
    print("-----------------get defered fields",car.get_deferred_fields())


gets()
# saves()