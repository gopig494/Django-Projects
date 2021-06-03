from django.contrib import admin
from studentapp.models import studentdetails

# Register your models here.
class listofdetails(admin.ModelAdmin):
	list=['student_register_no','student_name','student_address']
	
admin.site.register(studentdetails,listofdetails)
