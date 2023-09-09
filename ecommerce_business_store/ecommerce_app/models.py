from django.db import models

class Customer(models.Model):
    first_name = models.fields.CharField(max_length=10)
    last_name = models.fields.CharField(max_length=10)
    email = models.fields.EmailField()
    phone = models.fields.CharField(max_length=12)