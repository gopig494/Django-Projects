from rest_framework import serializers
from ecommerce_app.models import Customer

class serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_phone(self, phone):
        if len(phone) < 10:
            raise serializers.ValidationError("The phone number must be 10 digits")
        return phone

    def validate(self, data):
        if 'com' not in data.get('email'):
            raise serializers.ValidationError("Invalid email..!")
        return data