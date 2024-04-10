from rest_framework.decorators import api_view
from rest_framework.response import Response
from customer.models import FieldCheck
from rest_framework import status
from .serializers import FieldCheckSerializer

@api_view(["POST", "GET"])
def check_fields(request):
    if request.method == "POST":
        serializer_response = FieldCheckSerializer(data = request.data)
        if serializer_response.is_valid():  
            print("--------------",serializer_response)
            serializer_response.save()
            return Response({"status": "success","data": serializer_response.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_response.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("not working")