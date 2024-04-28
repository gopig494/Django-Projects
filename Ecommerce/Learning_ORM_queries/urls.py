from django.urls import path,include
from Learning_ORM_queries.views import *

urlpatterns = [
    path("creating_blog/",creating_blog),
    path("get_blog/",get_blog),
    path("update_blog/",update_blog),
    path("creating_entry/",creating_entry),
    path("get_entry/",get_entry),
    path("create_production/",create_production),
    path("get_production/",get_production),
    path("delete_production/",delete_production),
] 


