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
