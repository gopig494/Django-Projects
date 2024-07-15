from django.urls import path
from .views import *

urlpatterns = [
    path("product-list/",product_list,name = "product_list"),
    path("add-to-cart/",add_to_cart,name = "add_to_cart"),
    path("delete-cart/",delete_cart,name="delete-cart"),
    path("sign-up",sign_up,name='sign_up'),
    path("login",log_in,name='login'),
    path("add_cart_byid/<int:cart_id>",add_cart_by_id)
]
