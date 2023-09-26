from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from ecommerce_app.models import Customer
from ecommerce_app.serializer import Customerserializer,Customerlogin,CustomerRegisterSerializer
import ecommerce_app
from rest_framework.views import APIView
from rest_framework import viewsets,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BaseAuthentication 
from django.core.paginator import Paginator
import django

@api_view(["GET","POST","PUT","DELETE","PATCH"])
def get_customer_info(request):
    if request.method == "GET":
        obj2 = Customer.objects.all()
        # obj2 = Customer.objects.filter(nationality = 2)
        page = request.GET.get('page',1)
        page_size = 2
        pagenation = Paginator(obj2,page_size)
        try:
            ser = Customerserializer(pagenation.page(page), many = True)
        except django.core.paginator.EmptyPage:
            return Response({"status":"failed","message":"no data found"},status = status.HTTP_404_NOT_FOUND)
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

@api_view(["POST"])
def login(request):
    validate_data = Customerlogin(data = request.data)
    if validate_data.is_valid():
        data = validate_data.data
        auth = authenticate(username = data.get("username"),password = data.get("password"))
        if auth:
            token,status_ = Token.objects.get_or_create(user = auth)
            return Response({"status":"success","message":"Logged in successfully","token":str(token)},status=status.HTTP_200_OK)
        else:
            return Response({"status":"failed","message":"email or password is invalid"},status=status.HTTP_401_UNAUTHORIZED)    
    else:
        return Response({"status":"failed","message":validate_data.errors},status=status.HTTP_400_BAD_REQUEST)
    
class CustomerCrud(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self,request):
        data = Customerserializer(data = request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)
        
    def get(self,request):
        obj2 = Customer.objects.all()
        # obj2 = Customer.objects.filter(nationality = 2)
        ser = Customerserializer(obj2, many = True)
        return Response(ser.data)
    
    def put(self,request):
        exe_data = Customer.objects.get(id=request.data.get('id'))
        update_va = Customerserializer(exe_data,data = request.data)
        if update_va.is_valid():
           update_va.save()
           return Response(update_va.data)
        else:
            return Response(update_va.errors) 
        
    def patch(self,request):
        exe_data = Customer.objects.get(id=request.data.get('id'))
        update_va = Customerserializer(exe_data,data = request.data, partial = True)
        if update_va.is_valid():
           update_va.save()
           return Response(update_va.data)
        else:
            return Response(update_va.errors)
        
    def delete(self,request):
        try:
            del_obj = Customer.objects.get(id = request.data.get("id"))
            del_obj.delete()
            return Response({"status":"success","message":"Customer info deleted successfully"})
        except ecommerce_app.models.Customer.DoesNotExist:
            return Response({"status":"failed","message":f"The customer {request.data.get('id')} is not found."})

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = Customerserializer
    queryset = Customer.objects.all()

    def list(self, request):
        searchdata = request.data.get('searchdata')
        if searchdata:
            self.queryset = self.queryset.filter(first_name__startswith = searchdata)
        data = Customerserializer(self.queryset, many = True)
        return Response({"status":"success","data":data.data},status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def register_customer(request):
    serializer_data = CustomerRegisterSerializer(data = request.data)
    if serializer_data.is_valid():
        serializer_data.save()
        return Response({"status":"success","data":serializer_data.data},status=status.HTTP_201_CREATED)
    else:
        return Response({"status":"failed","message":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)