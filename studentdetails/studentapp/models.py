from django.db import models

# Create your models here.

class studentdetails(models.Model):
	student_register_no=models.IntegerField()
	student_name=models.CharField(max_length=20)
	student_address=models.CharField(max_length=200)
