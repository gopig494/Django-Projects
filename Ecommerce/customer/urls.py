"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from customer import views
from customer import api_url

# app_name = "polls"

urlpatterns = [
    path('register/', views.register),
    path('register/reg/', views.register),
    path('login/', views.login),
    path("api/method/",include(api_url)),
    path("dynamic_url/<str:id>/<int:iff>",views.dynamic_url,name="dynamic_url"),
    path("dynamic_ur/",views.dynamic_url,name="dy"),
    path("<int:question_id>/<int:q_id>/vote/", views.vote, name="vote"),
    path("generic/list_view/", views.IndexView.as_view(), name="generic_list"),
    path("generic/detail_view/<int:pk>", views.DetailView.as_view(), name="generic_detail")
]
