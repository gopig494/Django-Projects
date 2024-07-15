from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name","price","old_price"]
    list_filter = ["product_name","price","old_price"]
    list_per_page = 100

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)