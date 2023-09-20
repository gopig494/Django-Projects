from django.contrib import admin
from ecommerce_app.models import Customer,CustomerAddress,Nationality

class FetchCustomer(admin.ModelAdmin):
    data = ["first_name","last_name","email","phone"]

admin.site.register(Customer,FetchCustomer)
admin.site.register(CustomerAddress)
admin.site.register(Nationality)