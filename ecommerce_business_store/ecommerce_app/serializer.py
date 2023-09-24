from rest_framework import serializers
from ecommerce_app.models import Customer,Nationality
from django.contrib.auth.models import User

class Customerlogin(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class CustomerRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data.get("username")).exists():
            raise serializers.ValidationError("username is already taken")
        elif User.objects.filter(email = data.get("email")).exists():
            raise serializers.ValidationError("email is already taken")
        elif not data.get("password"):
            raise serializers.ValidationError("password not found")
        return data

    def create(self, data):
        create_data = User.objects.create(username = data.get('username'),email = data.get('email'))
        create_data.set_password(data.get("password"))
        create_data.save()
        return data

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
    