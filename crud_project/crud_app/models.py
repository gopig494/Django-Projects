from django.db import models

# Create your models here.

class Customer(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)