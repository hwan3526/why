from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import *
from .serializers import *
from .forms import BlogForm, UserForm

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    

def board(request):
    return render(request, 'board.html')

def login(request):
    form = UserForm()
    return render(request, 'login.html', {'form': form})

def write(request):
    form = BlogForm()
    return render(request, 'write.html', {'form': form})

def board_detail(request):
    return render(request, 'board-detail.html')
