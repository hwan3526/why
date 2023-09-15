from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from . models import *
from .serializers import *
from .forms import BlogForm, UserForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views import View
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

def extract_image_src(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tag = soup.find('img')
    
    if image_tag:
        src_attribute = image_tag.get('src', '')
        return src_attribute
    else:
        return ''

def board(request, category_id=None):
    theme = 'dark'
    is_logined = False
    topics = Category.objects.all()

    base_query = Q(Q(user_id=request.user.id) & Q(in_private=True)) | Q(~Q(user_id=request.user.id) & Q(in_private=False))

    if request.user.id == 1:
        posts = Blog.objects.filter(
            Q(category_id=category_id) if category_id else Q(),
            temporary=False
        ).order_by('-upload_date__date', '-count')
    else:
        posts = Blog.objects.filter(
            base_query,
            Q(category_id=category_id) if category_id else Q(),
            temporary=False
        ).order_by('-upload_date__date', '-count')

    first_post = posts.first()

    for post in posts:
        post.image_tag = extract_image_src(post.content)

    if first_post:
        first_img = extract_image_src(first_post.content)
    else:
        first_img = ''

    context = {
        'theme': theme, 
        "is_logined": is_logined, 
        'first_post': first_post, 
        'posts': posts[1:], 
        'img': first_img,
        'topics' : topics
    }

    return render(request, 'board.html', context)

def board_view(request):
    return redirect('board')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})

def user_login(request):
    is_logined = True

    if request.user.is_authenticated:
        return redirect('board')
    else:
        form = UserForm(data=request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('board')
        return render(request, 'board.html', {'form': form, "is_logined":is_logined})

def logout(request):
    logout(request)
    return render(request, "board.html", {"is_logined": False})

@login_required(login_url='login')
def write(request, blog_id=None):
    theme = 'light'
    topics = Category.objects.all()

    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id)
    else:
        blog = Blog.objects.filter(user=request.user.id, temporary=True).order_by('-upload_date').first()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)

            if 'delete-button' in request.POST:
                blog.delete() 
                return redirect('board') 

            title = request.POST['title']
            content = request.POST['content']

            in_private = False
            private_value = request.POST.get('in_private')
            if private_value:
                in_private = True

            category_id = request.POST['topic']
            blog.category_id = category_id

            temporary = False

            if 'temp-save-button' in request.POST:
                blog.temporary = True
            else:
                blog.temporary = False

            temporary = blog.temporary
            count = 0
            finduser = User.objects.get(pk=request.user.id)
            blog.user = finduser

            if blog.id:
                blog.save()
            else:
                blog = Blog.objects.create(user_id=finduser.id, category_id=category_id, in_private=in_private, temporary=temporary, count=count, title=title, content=content)
            return redirect('board_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)

    context = {
        'theme': theme,
        'form': form,  
        'post': blog, 
        'edit_mode': blog_id is not None, 
        'MEDIA_URL': settings.MEDIA_URL,
        'topics' : topics,
    } 

    return render(request, 'write.html', context)

@login_required(login_url='login')
def board_delete(request, blog_id=None):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.user.id == 1 or request.user.id == blog.user.id:
        if request.method == 'POST': 
            if 'delete-button' in request.POST:
                blog.delete()
                return redirect('board')

def board_detail(request, blog_id=None):
    theme = 'light'

    blog = get_object_or_404(Blog, pk=blog_id)
    topics = Category.objects.all()

    if blog.user.id != request.user.id and blog.in_private == False:
        blog.count += 1
        blog.save()

    author_user = User.objects.get(id=blog.user.id)

    prev_blog = Blog.objects.filter(id__lt=blog.id, temporary=False, in_private=False).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt=blog.id, temporary=False, in_private=False).order_by('id').first()

    recommended_blogs = Blog.objects.filter(category=blog.category, temporary=False, in_private=False).exclude(id=blog.id).order_by('-upload_date')[:2]

    for recommended_blog in recommended_blogs:
        recommended_blog.image_tag = extract_image_src(recommended_blog.content)
    
    comment_form = None
    if request.user:        
        comment_form = CommentForm()

    comments = Comment.objects.filter(blog_id = blog_id)

    context = {
        'theme': theme, 
        'blog': blog,
        'author_name': author_user.username,
        'previous_post': prev_blog,
        'next_post': next_blog,
        'recommended_posts': recommended_blogs,
        'MEDIA_URL': settings.MEDIA_URL,
        'topics' : topics,
        'comment_form' : comment_form,
        'comments' : comments,
    }

    return render(request, 'board-detail.html', context)

class image_upload(View):
    def post(self, request):
        file = request.FILES['file']
        filepath = 'uploads/' + file.name
        filename = default_storage.save(filepath, file)
        file_url = settings.MEDIA_URL + filename
        return JsonResponse({'location': file_url})
    
@login_required(login_url='login')
def comment_write(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = User.objects.get(pk=request.user.id)
            comment.blog = blog
            comment.save()
            return redirect('board_detail', blog_id = blog.id)
    else:
        comment_form = Comment()
    return render(request, 'board-detail.html', {"comment_form": comment_form})

@login_required(login_url='login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    blog_id = comment.blog.id
    if request.user.id == comment.user.id or request.user.id == 1:
        comment.delete()
    return redirect('board_detail', blog_id = blog_id)

@login_required(login_url='login')
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    blog_id = comment.blog.id
    if request.method == 'POST':
        edited_comment = request.POST.get('edited_comment')
        comment = Comment.objects.get(id=comment_id)
        comment.comment = edited_comment
        comment.save()
        return HttpResponse(status=200)
    
    return redirect('board_detail', blog_id = blog_id)