from django import forms

class CustomerInfo(forms.Form):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)
