from django.contrib import admin
from Learning_ORM_queries.models import *

# Register your models here.

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ["name","tagline"]

class EntryModelAdmin(admin.ModelAdmin):
    list_display = ["blog","headline"]

        

admin.site.register(Blog,BlogModelAdmin)
admin.site.register(Author)
admin.site.register(Entry,EntryModelAdmin)
admin.site.register(Production)
admin.site.register(Location)
admin.site.register(Car)
admin.site.register(Product)
# admin.site.register(AbstractCar)
admin.site.register(LearnMeta)
admin.site.register(LearnManaged)
admin.site.register(Person)
admin.site.register(LearnModel)
admin.site.register(LearnValidate)
admin.site.register(BankCustomer)










