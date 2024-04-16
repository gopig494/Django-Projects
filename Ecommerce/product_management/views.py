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
    from django.db import IntegrityError
    customer_id = 1
    while True:
        try:
            car = Car(id=customer_id,title = "chsssssseck",price=200,model_nos="gocommscs")
            car.save(force_insert = True,using='secondary')  
            print("-----------------before refreshing from db")
            # car.refresh_from_db()
            # car.arefresh_from_db()
            break
        except IntegrityError: 
            customer_id += 1
            continue

def update():
    car = Car.objects.get(id=1)
    print("-----------------car--first>",car)
    print("-----------------get defered fields",car.get_deferred_fields())
    car.price = 123
    car.save(force_update = True,update_fields = ["price"],using='secondary')
    print("-----------------car--first>",car)
    print("-----------------get defered fields",car.get_deferred_fields())

def gets():
    car = Car.objects.defer("price").first()
    print("-----------------car--first>",car)
    print("-----------------get defered fields",car.get_deferred_fields())


# gets()
# saves() 
# update() 