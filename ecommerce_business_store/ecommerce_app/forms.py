from django import forms
from ecommerce_app.models import Customer

class CustomerInfo(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        # exclude = ["phone"] 

# class CustomerInfo(forms.Form):
#     first_name = forms.CharField(max_length=10)
#     last_name = forms.CharField(max_length=10)
#     email = forms.EmailField()
#     phone = forms.CharField(max_length=12)
