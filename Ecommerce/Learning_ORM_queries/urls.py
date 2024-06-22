from django.urls import path,include
from Learning_ORM_queries.views import *
from Learning_ORM_queries.views_2 import *

urlpatterns = [
    path("creating_blog/",creating_blog),
    path("get_blog/",get_blog),
    path("update_blog/",update_blog),
    path("creating_entry/",creating_entry),
    path("get_entry/",get_entry),
    path("create_production/",create_production),
    path("get_production/",get_production),
    path("delete_production/",delete_production),
    path("get_entry_api/",get_entry_api),
    path("learn_extra/",learn_extra),
    path("lock_transaction/",lock_transaction),
    path("and_or/",and_or),
    path("crud/",crud),
    path("more_functions/",more_functions),
    path("diff_filters/",diff_filters),
    path("revise/",revise),
    path("learn_meta/",learn_meta),
    path("learn_model/",learn_model),
    path("validate_model/",validate_model),
    path("model_details/<int:pk>/",validate_model,name="model_detail"),
    path("get_human_readble_values/",get_human_readble_values),
    path("raw_sql_learning/",raw_sql_learning),
    path("learn_sql_store_procedure/",learn_sql_store_procedure),
    path("model_inheritance/",model_inheritance),
    path("learn_aggerigation/",learn_aggerigation),
    path("learn_search/",learn_search),
    path("learn_database_functions/",learn_database_functions),
    path("learn_query_expressions/",learn_query_expressions),
    path("learn_expression_api/",learn_expression_api),
    path("learn_datetime_database_functions/",learn_datetime_database_functions),
    
] 


