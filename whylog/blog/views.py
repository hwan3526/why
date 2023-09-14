from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from . models import *
from .serializers import *
from .forms import BlogForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.views import View
from django.core.files.storage import default_storage
from django.http import JsonResponse

from bs4 import BeautifulSoup

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

    
def board(request, topic=None):
    theme = 'dark'
    is_logined = False
    if topic:
        posts = Blog.objects.filter(Category=topic, temporary=False).order_by('-upload_date', '-count')
        first_post = posts[0]
    else:
        posts = Blog.objects.filter(temporary=False).order_by('-upload_date', '-count')
        first_post = posts[0]
    return render(request, 'board.html', {'theme': theme, "is_logined": is_logined, 'first_post': first_post, 'posts': posts[1:]})

def board_view(request):
    return redirect('board')

def login(request):
    is_logined = True

    if request.user.is_authenticated:
        return redirect('blog:board')
    else:
        form = UserForm(data=request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:board')
        return render(request, 'board.html', {'form': form, "is_logined":is_logined})

def logout(request):
    logout(request)
    return render(request, "board.html", {"is_logined": False})

def update_blog(request, blog_id):
    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id)
    else:
        blog = Blog.objects.filter(user_id=request.user.id, temporary=False).order_by('-upload_date').first()

def write(request):
    theme = 'light'

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user.id
            title = request.POST['title']
            content = request.POST['content']
            in_private = False
            temporary = False
            count = 0
            category_id = 1
            user_id_id = request.user.id
            blog = Blog.objects.create(user_id_id=user_id_id, category_id=category_id, in_private=in_private, temporary=temporary, count=count, title=title, content=content)
            blog.save()
            return redirect('board_detail', blog_id=blog.id)
    else:
        form = BlogForm()

    context = {
        'theme': theme,
        'form': form,  
        # 'blog': blog, 
        # 'edit_mode': blog_id is not None, 
        # 'MEDIA_URL': settings.MEDIA_URL,
    } 

    return render(request, 'write.html', context)

def board_detail(request, blog_id=None):
    theme = 'light'
    blog = get_object_or_404(Blog, pk=blog_id)

    blog.count += 1
    blog.save()

    prev_blog = Blog.objects.filter(id__lt=blog.id, temporary=False).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt=blog.id, temporary=False).order_by('id').first()

    recommended_blogs = Blog.objects.filter(category=blog.category, temporary=False).exclude(id=blog.id).order_by('-upload_date')[:2]

    for recommended_blog in recommended_blogs:
        soup = BeautifulSoup(recommended_blog.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_blog.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'theme': theme, 
        'blog': blog,
        'previous_post': prev_blog,
        'next_post': next_blog,
        'recommended_posts': recommended_blogs,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'board-detail.html', context)

def image_upload(View):
    def post(self, request):
        file = request.FILES['file']
        filepath = 'uploads/' + file.name
        filename = default_storage.save(filepath, file)
        file_url = settings.MEDIA_URL + filename
        return JsonResponse({'location': file_url})
