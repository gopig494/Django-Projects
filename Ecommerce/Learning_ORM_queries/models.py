from django.db import models
from datetime import date

# Create your models here.

from datetime import date

from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200,unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)
    modified = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.headline
  
class Production(models.Model):
    name = models.CharField(max_length=100)
    values = models.JSONField(null=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,related_name="entry_forign")
    entries = models.ManyToManyField(Entry)

# Review models

class Location(models.Model):
    city = models.CharField(verbose_name="Current City",max_length=20)

    # forign key is many to one field

    blog = models.ForeignKey(Blog,verbose_name="Blog",on_delete=models.CASCADE)

    # we can create self relationship

    # first way

    parent_location = models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,default=None)

    def __str__(self):
        return self.city

# use absraction 

# we can use the model anyware in the project with the fieldnames

# now the example use the same file to explore

class AbstractCar(models.Model):
    car_model = models.CharField(max_length=100)

    class Meta:
        abstract = True

# here the car model having both car_model field and colour field

# just reusability takes place 

class Car(AbstractCar):
    colour = models.CharField(max_length=40)