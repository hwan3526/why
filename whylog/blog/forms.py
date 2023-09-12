from django import forms
from .models import Blog, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title' , 'content']