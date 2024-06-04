from typing import Any
from .models import *
from django import forms


class CleanForm(forms.ModelForm):
    class Meta:
        model = LearnValidate
        fields = "__all__"
    
    # def clean(self) -> dict[str, Any]:
    #     try:
    #         self.validate_unique(exclude=['id'])
    #     except forms.ValidationError as e:
    #         self.add_error('uni_field', e)
    #     return super().clean()

    # def clean_age(self):
    #     age = self.cleaned_data.get("age")
    #     if age  == 1:
    #         print("---entered")
    #         # raise forms.ValidationError("Age can't be 1.")
    #         raise forms.ValidationError("E-mail is already exists.Please try different email.")  
    #     return age
    
    # def validate_unique(self, exclude: Collection[str] | None = ...) -> None:
    #     uni_field_data = self.cleaned_data.get("uni_field")
    #     if uni_field_data == 1 :
    #         raise forms.ValidationError('unique error')
    #     super().validate_unique()   