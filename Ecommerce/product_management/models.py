from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    mrp = models.FloatField()
    price = models.FloatField()
    tax_percentage = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="images")
