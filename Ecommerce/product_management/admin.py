from django.contrib import admin
from product_management.models import *
# Register your models here.

class CategoryInline(admin.TabularInline):
    model = Product
    extra = 1

class StockEntryLine(admin.TabularInline):
    model = StockEntryItems
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    # fields = ["price","title","image"]
    fieldsets = [(None,{"fields":["title"]}),
                ("Section 1",{"fields":["price","image"]}),
                ("Section 2",{"fields":["category","mrp","tax_percentage","description"]})]
    list_display = ["title","price","mrp"]

class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [CategoryInline] 

class StockEntryModelAdmin(admin.ModelAdmin):
    inlines = [StockEntryLine]


admin.site.register(Product,ProductAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Article2)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Category,CategoryModelAdmin)
admin.site.register(StockEntry,StockEntryModelAdmin)
admin.site.register(StockEntryItems)
