from typing import Any
from django.db import models

class Nationality(models.Model):
    country_name = models.CharField(max_length = 50)
    short_form = models.CharField(max_length = 10, default = "IND")

    def __str__(self) -> str:
        return f"{self.country_name}"

class Customer(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    nationality = models.ForeignKey(Nationality,on_delete=models.CASCADE)
     
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class CustomerAddress(models.Model):
    Customer = models.ForeignKey(Customer,null=True,blank=True,on_delete=models.CASCADE)
    address = models.CharField(max_length = 200)
    district = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    pin_code = models.IntegerField()
