from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content","image"]

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Add comment...'}))
    class Meta:
        model = Comment
        fields = ['body',]