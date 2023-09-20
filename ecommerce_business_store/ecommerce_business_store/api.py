from django.urls import path,include
from ecommerce_app import api

urlpatterns = [
    path('get_customer_info',api.get_customer_info),
    path('login',api.login),
    path('customer',api.CustomerCrud.as_view())
]