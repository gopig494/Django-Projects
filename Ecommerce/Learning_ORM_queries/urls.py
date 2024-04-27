from django.urls import path,include
from Learning_ORM_queries.views import *

urlpatterns = [
    path("creating_blog/",creating_blog),
    path("get_blog/",get_blog),
    path("creating_entry/",creating_entry),
    path("get_entry/",get_entry),
] 
