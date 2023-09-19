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
from django.dispatch import receiver
from django.db.models.signals import post_save
from collections import defaultdict
from bs4 import BeautifulSoup
import openai
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
    
def get_notifications(request):
    finduser = User.objects.get(pk=request.user.id)
    recent_alarms = Alarm.objects.filter(target_user=finduser, isRead=False)

    notifications = {
        'recent_alarms': len(recent_alarms),
        'blog_comment': [],
        'blog_like': [],
        'comment_like': [],
    }

    for alarm in recent_alarms:
        if alarm.comment_id:
            comment = Comment.objects.get(pk=alarm.comment_id)
            blog = Blog.objects.get(pk=comment.blog.id)
            blog_comment = {"blog": blog, "comment": comment, "alarm_id": alarm.id}
            notifications['blog_comment'].append(blog_comment)

        if alarm.like_id:
            likes = Like.objects.filter(pk=alarm.like_id)

            for like in likes:
                if like.blog:
                    find_like_blog = Blog.objects.get(pk=like.blog.id)
                    blog_like = {"blog": find_like_blog, "alarm_id": alarm.id}
                    notifications['blog_like'].append(blog_like)

                if like.comment:
                    comment = Comment.objects.get(pk=like.comment.id)
                    blog = Blog.objects.get(pk=comment.blog.id)
                    comment_like = {"comment": like.comment, "alarm_id": alarm.id, "blog_id": blog.id}
                    notifications['comment_like'].append(comment_like)

    return {'recent_alarms': notifications}

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        if Comment:
            Alarm.objects.create(
                user=instance.user,
                target_user=instance.blog.user, 
                comment=instance,
                like=None,
            )

@receiver(post_save, sender=Like)
def create_Like_notification(sender, instance, created, **kwargs):
    if created:
        if instance.blog:
            Alarm.objects.create(
                user=instance.user,
                target_user=instance.blog.user, 
                comment=None,
                like=instance,
            )
        if instance.comment:
            Alarm.objects.create(
                user=instance.user,
                target_user=instance.comment.user, 
                comment=None,
                like=instance,
            )

@login_required
def alarm_read(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    if request.method == 'POST':
        alarm.isRead = True
        alarm.save()
    return HttpResponse(status=200)

def board(request, category_id=None):
    theme = 'dark'
    is_logined = False
    topics = Category.objects.all()

    if request.user.id == 1:
        posts = Blog.objects.filter(
            Q(category_id=category_id) if category_id else Q(),
            temporary=False
        ).order_by('-upload_date__date', '-count')
    else:
        posts = Blog.objects.filter(
            Q(Q(user_id=request.user.id)) | Q(~Q(user_id=request.user.id) & Q(in_private=False)),
            Q(category_id=category_id) if category_id else Q(),
            temporary=False
        ).order_by('-upload_date__date', '-count')

    for post in posts:
        post.comments = Comment.objects.filter(Q(blog_id=post.id)).count()
        if extract_image_src(post.content):
            post.image_tag = extract_image_src(post.content)
        else:
            post.image_tag = 'media/dudon.png'

    notifications = []
    if request.user.is_authenticated:
        notifications = get_notifications(request)['recent_alarms']

    context = {
        'theme': theme, 
        "is_logined": is_logined, 
        'posts': posts, 
        'topics' : topics,
        'notifications': notifications,
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

            private_value = request.POST.get('in_private')

            if private_value:
                blog.in_private = True
            else:
                blog.in_private = False

            category_id = request.POST['topic']
            blog.category_id = category_id

            if 'temp-save-button' in request.POST:
                blog.temporary = True
            else:
                blog.temporary = False

            blog.count = 0
            finduser = User.objects.get(pk=request.user.id)
            blog.user = finduser

            blog.save()

            return redirect('board_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)

    notifications = []
    if request.user.is_authenticated:
        notifications = get_notifications(request)['recent_alarms']

    context = {
        'theme': theme,
        'form': form,  
        'post': blog, 
        'edit_mode': blog_id is not None, 
        'MEDIA_URL': settings.MEDIA_URL,
        'topics' : topics,
        'notifications': notifications,
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
        if extract_image_src(recommended_blog.content):
            recommended_blog.image_tag = extract_image_src(recommended_blog.content)
        else:
            recommended_blog.image_tag = 'media/dudon.png'
    
    comment_form = None
    if request.user:        
        comment_form = CommentForm()

    comments = Comment.objects.filter(blog_id = blog_id).order_by('upload_date')

    like_post = None
    liked_comments = None
    
    if request.user.is_authenticated:
        finduser = User.objects.get(pk=request.user.id)
        liked_comment_ids = Like.objects.filter(user=finduser, comment__in=comments).values_list('comment_id', flat=True)
    else:
        liked_comment_ids = Like.objects.filter(comment__in=comments).values_list('comment_id', flat=True)

    like_post_user_ids = Like.objects.filter(blog=blog).values_list('user', flat=True)
    liked_comments = Like.objects.filter(comment__in=comments)
    comment_like_count = defaultdict(int)

    for like in liked_comments:
        comment_id = like.comment_id
        comment_like_count[comment_id] += 1

    comment_like_count = dict(comment_like_count)

    notifications = []
    if request.user.is_authenticated:
        notifications = get_notifications(request)['recent_alarms']

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
        'like_post' : like_post_user_ids,
        'liked_comment' : liked_comment_ids,
        'comment_like_count' : comment_like_count,
        'notifications': notifications,
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

@login_required(login_url='login')
def like_comment_toggle(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    blog_id = comment.blog.id

    if request.method == 'POST':
        finduser = User.objects.get(pk=request.user.id)
        findLiked = Like.objects.filter(user=finduser, comment=comment)

        if findLiked:
            findLiked.delete()
        else:
            liked = Like.objects.create(user=finduser, comment=comment)

        return HttpResponse(status=200)

    return redirect('board_detail', blog_id = blog_id)

@login_required(login_url='login')
def like_blog_toggle(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        finduser = User.objects.get(pk=request.user.id)
        findLiked = Like.objects.filter(user=finduser, blog=blog)

        if findLiked:
            findLiked.delete()
        else:
            liked = Like.objects.create(user=finduser, blog=blog)

        return HttpResponse(status=200)

    return redirect('board_detail', blog_id = blog_id)

def search(request):
    theme = 'dark'
    is_logined = False
    topics = Category.objects.all()

    search_text = request.GET.get('searchBox-input')

    blog_results = Blog.objects.filter(
        Q(title__icontains=search_text) | Q(content__icontains=search_text)  
    )

    comment_results = Comment.objects.filter(
        Q(comment__icontains=search_text)
    )

    for comment in comment_results:
        comment.blog_info = Blog.objects.get(id=comment.blog_id)

    blog_list = list(blog_results)
    for comment in comment_results:
        blog_list.append(comment.blog_info)

    for post in blog_list:
        if extract_image_src(post.content):
            post.image_tag = extract_image_src(post.content)
        else:
            post.image_tag = 'media/dudon.png'

    notifications = []
    if request.user.is_authenticated:
        notifications = get_notifications(request)['recent_alarms']

    context = {
        'theme': theme, 
        "is_logined": is_logined, 
        'posts': blog_list, 
        'topics' : topics,
        'notifications': notifications,
    }

    return render(request, 'board.html', context)

openai.api_key = settings.API_KEY

def autocomplete(request):
    if request.method == "POST":
        
        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return redirect('board')