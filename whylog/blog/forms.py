from django import forms
from .models import Blog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title' , 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목'})
        }
        