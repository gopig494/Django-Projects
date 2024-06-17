from django.db import models
from .models import *
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField,SearchVector

class SearchKey(models.Model):
    search_keyword = models.CharField(max_length=100)
    full_description = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE,blank=True)
    proxy_learn = models.ManyToManyField(ProxyLearn,blank=True)
    # we can use searchvector and seachquery without specifing these by the performance is poor

    # so we have to use the searchvector field to see real search performance

    #way 2 reference

    # in this search vector field the all above fields values are store by default the model get updated or inserted.

    # we can manuaaly update the field data by using the query set like below

    # SearchKey.objects.update(search_vector = SearchVector("search_keyword","full_description"))

    search_vector = SearchVectorField(null=True,blank=True,editable=False)

    def __str__(self):
        return self.search_keyword
    
    class Meta:
        # it will create full text to search for the search_keyword and full_description fields on search_vector_idx the optimized data will be stored

        indexes = [
            #way 1

            # you can see the view2.py on that file we have use search vector , search query, searchHeadLinequery

            # these are queries can be used without the below indexing but for the performance we must specify the indexing

           GinIndex(
                SearchVector("search_keyword", "full_description", config="english"),
                name="search_vector_idx",
            ),
            #way 2
            GinIndex(fields=['search_vector'])
        ]

class QueryExps(models.Model):
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    nos = models.IntegerField()
    description = models.TextField()
    verified = models.BooleanField()

    def __str__(self):
        return self.name