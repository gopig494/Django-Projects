from django import forms
from crud_app.models import Customer

class CustomerRegister(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

# class CustomerRegister(forms.Form):
#     user_id = forms.IntegerField()
#     user_name = forms.CharField(max_length=255)
#     full_name = forms.CharField(max_length=255)