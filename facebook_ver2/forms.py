from django import forms
from .models import Profiles
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = Profiles
        fields = ['username','email','password1','password2']

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['avatar','first_name','last_name','email','bio']