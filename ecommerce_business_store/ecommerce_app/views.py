from django.shortcuts import render,redirect
from django.http import HttpResponse
from ecommerce_app.models import Customer
from ecommerce_app.forms import CustomerInfo
from django.views.generic import View

class ClassView(View):
    def get(self,request):
        return HttpResponse("working")

def index(request):
    emp_all_details = Customer.objects.all()
    return render(request,"ecommerce_app/index.html",context={"emp_details":emp_all_details})

def customer_register(request):
    form = CustomerInfo()
    if request.method == "POST":
        form = CustomerInfo(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/ecommerce/views/")
    return render(request,'ecommerce_app/customer_register.html',context={"cust_register":form})

def update_customer(request,id):
    cust = Customer.objects.get(id=id)
    if request.method == "POST":
        update_info = CustomerInfo(request.POST,instance=cust)
        if update_info.is_valid():
            update_info.save()
            return redirect("/ecommerce/views")
    return render(request,'ecommerce_app/update.html',context={"cust_info":cust})

def delete_customer(request,id):
    cust = Customer.objects.get(id=id)
    cust.delete()
    return redirect("/ecommerce/views")


