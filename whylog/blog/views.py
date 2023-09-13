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
    theme = 'dark'
    return render(request, 'board.html', {'theme': theme})


def login(request):
    form = UserForm()
    return render(request, 'login.html', {'form': form})

def write(request):
    form = BlogForm()
    theme = 'light'
    return render(request, 'write.html', {'form': form, 'theme': theme})

def board_detail(request):
    theme = 'light'
    return render(request, 'board-detail.html', {'theme': theme})



# def login(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('board.html')
#     else:
#         form = UserForm()
#         return render(request, 'login.html', {'form': form})


# def write(request):
#     if request.method == "POST":
#         title = request.POST["title"]
#         content = request.POST["content"]
#         Blog.objects.create(title=title, content=content)
#         user = Blog()
#         user.save()
        
#         return render(request, "write.html")    
