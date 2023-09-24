from django.urls import path,include
from ecommerce_app import api
from rest_framework.routers import DefaultRouter
from ecommerce_app.api import CustomerViewSet

router = DefaultRouter()
router.register(r"_info",CustomerViewSet,basename="_info")

urlpatterns = [
    path('customer_crud',include(router.urls)),
    path('get_customer_info',api.get_customer_info),
    path('login',api.login),
    path('customer',api.CustomerCrud.as_view()),
    path('register',api.register_customer)
]