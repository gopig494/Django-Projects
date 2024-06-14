from django.db import models
from .models import *

class SearchKey(models.Model):
    search_keyword = models.CharField(max_length=100)
    full_description = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE,blank=True)
    proxy_learn = models.ManyToManyField(ProxyLearn,blank=True)

    def __str__(self):
        return self.search_keyword