from django.shortcuts import render,redirect
from django.http import HttpResponse
from crud_app.forms import CustomerRegister
from crud_app.models import Customer

# Create your views here.

def login(request):
    return render(request,"crud_app/login.html",context={"register_from":CustomerRegister()})

def create_customer(request):
    if request.method == "POST":
        form = CustomerRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/crud/view/")
        else:
            return render(request,form)
    return render(request,"crud_app/login.html",context={"register_from":CustomerRegister()})

def view_customer(request):
    all_data = Customer.objects.all()
    if all_data:
        return render(request,"crud_app/views.html",context = {"all_data":all_data})
    else:
        return redirect("/crud/create/")

def update_customer(request,id):
    cust = Customer.objects.get(id=id)
    if request.method == "POST":
        form_ins = CustomerRegister(request.POST,instance=cust)
        if form_ins.is_valid():
            form_ins.save()
            return redirect("/crud/view/")
    return render(request,'crud_app/update.html',context={"cust_info":cust})

def delete_customer(request,id):
    exe_info = Customer.objects.get(id=id)
    if exe_info:
        exe_info.delete()
    return redirect("/crud/view/")

# def update_customer(request,id):
#     cust = Customer.objects.get(id=id)
#     if request.method == "POST":
#         update_info = CustomerInfo(request.POST,instance=cust)
#         if update_info.is_valid():
#             update_info.save()
#             return redirect("/ecommerce/views")
#     return render(request,'ecommerce_app/update.html',context={"cust_info":cust})

# def delete_customer(request,id):
#     cust = Customer.objects.get(id=id)
#     cust.delete()
#     return redirect("/ecommerce/views")

