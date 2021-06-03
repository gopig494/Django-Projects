from django import forms 
from studentapp.models import studentdetails

class fdetails(forms.ModelForm):
    class Meta:
        model=studentdetails
        fields='__all__'
        
        
