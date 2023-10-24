from django import forms
from .models import Profiles

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = '__all__'
        exclude =['user']