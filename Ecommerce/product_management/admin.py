from django.contrib import admin
from product_management.models import *
# Register your models here.

# StackedInline
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
    list_filter = ["tax_percentage","mrp","category"]
    search_fields = ["title","mrp","price"]

class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [CategoryInline] 

class StockEntryModelAdmin(admin.ModelAdmin):
    inlines = [StockEntryLine]

class FieldTypesCheckL2ModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_f": ["chr"]}

class FieldCheck3ModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"URL": ["title"],}

admin.site.register(Product,ProductAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Article2)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Category,CategoryModelAdmin)
admin.site.register(StockEntry,StockEntryModelAdmin)
admin.site.register(StockEntryItems)
admin.site.register(DiscountInfo)
admin.site.register(FieldTypesCheckL)
admin.site.register(FieldTypesCheckL2,FieldTypesCheckL2ModelAdmin)
admin.site.register(FieldCheck3,FieldCheck3ModelAdmin)
admin.site.register(CheckUUID)
# admin.site.register(Product_Forign)

