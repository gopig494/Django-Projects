from django.contrib import admin
from Learning_ORM_queries.models import *

# Register your models here.

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ["name","tagline"]

admin.site.register(Blog,BlogModelAdmin)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(Production)
