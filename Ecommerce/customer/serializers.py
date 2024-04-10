from rest_framework import serializers
from .models import FieldCheck
from product_management.models import Product

class FieldCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldCheck
        fields = "__all__"

    # def create(self, validated_data):
    #     print("-------validated_data.",validated_data)
    #     obj = FieldCheck.objects.create(_db_col = 2)
    #     obj.save()
    #     return obj

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        