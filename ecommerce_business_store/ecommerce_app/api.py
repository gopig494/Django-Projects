from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecommerce_app.models import Customer
from ecommerce_app.serializer import Customerserializer
import ecommerce_app

@api_view(["GET","POST","PUT","DELETE","PATCH"])
def get_customer_info(request):
    if request.method == "GET":
        obj2 = Customer.objects.all()
        # obj2 = Customer.objects.filter(nationality = 2)
        ser = Customerserializer(obj2, many = True)
        return Response(ser.data)
    elif request.method == "POST":
        data = Customerserializer(data = request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)
    elif request.method == "PUT":
        exe_data = Customer.objects.get(id=request.data.get('id'))
        update_va = Customerserializer(exe_data,data = request.data)
        if update_va.is_valid():
           update_va.save()
           return Response(update_va.data)
        else:
            return Response(update_va.errors) 
    elif request.method == "PATCH":
        exe_data = Customer.objects.get(id=request.data.get('id'))
        update_va = Customerserializer(exe_data,data = request.data, partial = True)
        if update_va.is_valid():
           update_va.save()
           return Response(update_va.data)
        else:
            return Response(update_va.errors) 
    elif request.method == "DELETE":
        try:
            del_obj = Customer.objects.get(id = request.data.get("id"))
            del_obj.delete()
            return Response({"status":"success","message":"Customer info deleted successfully"})
        except ecommerce_app.models.Customer.DoesNotExist:
            return Response({"status":"failed","message":f"The customer {request.data.get('id')} is not found."})