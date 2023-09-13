from django import forms
from .models import Blog, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'password': forms.TextInput(attrs={'placeholder': 'password'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title' , 'content']
        