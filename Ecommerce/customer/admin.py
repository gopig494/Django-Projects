from typing import Any
from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    using_1 = "sql_lite_db"
    using_2 = "postgresql_db"

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.save(using = self.using_2)
        # return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using_2)

    def get_queryset(self, request):
        print("-----------get queryset----------------------------------\n--------\n\n --works -- model admin--\n-----_++++++++++++++++")
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using_1)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


# Register your models here.
admin.site.register(FieldCheck)
admin.site.register(FieldCheck2)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product)
admin.site.register(TestMigrate)
# admin.site.register(TestMigrate2)

# we can separate certain table to different urls like by default the all models registerd like above is show in the route '/admin'

# the below model is viewed in different url which is config in urls.py

othersite = admin.AdminSite("othersite")
othersite.register(TestMigrate2)


