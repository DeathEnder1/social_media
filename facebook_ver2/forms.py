from django import forms
from .models import Profiles,Comment,Post
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = Profiles
        fields = ['username','email','password1','password2']

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['avatar','first_name','last_name','email','bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content","image"]

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Add comment...'}))
    class Meta:
        model = Comment
        fields = ['body']
        
class BlockForm(forms.Form):
    ACTIONS = [
        ('block', 'Block'),
        ('unblock', 'Unblock'),
    ]

    action = forms.ChoiceField(
        choices=ACTIONS,
        widget=forms.RadioSelect,
    )