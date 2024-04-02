from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(req):
    print("-->req",req)
    return HttpResponse("working from ecommerce app")