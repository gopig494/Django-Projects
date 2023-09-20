from rest_framework import serializers
from ecommerce_app.models import Customer,Nationality

class Customerlogin(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()

    def validate(self,data):
        if len(data.get('phone')) < 10:
            raise serializers.ValidationError("Phone number must 10 digits")

class Nationalityserializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ["id","short_form"]

class Customerserializer(serializers.ModelSerializer):
    nationality = Nationalityserializer()
    color_info = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = '__all__'
        # depth = 1

    def validate_phone(self, phone):
        if len(phone) < 10:
            raise serializers.ValidationError("The phone number must be 10 digits")
        return phone

    def validate(self, data):
        if 'com' not in data.get('email'):
            raise serializers.ValidationError("Invalid email..!")
        return data
    
    def get_color_info(self,obj):
        country_name = Nationality.objects.get(id = obj.nationality.id)
        return country_name.short_form
    