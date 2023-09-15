from django.db import models

from tinymce.models import HTMLField 

class Category(models.Model):
    category = models.CharField(max_length=50)

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_login_date = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100, default = None)

class Blog(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = HTMLField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_img = models.TextField()
    in_private = models.BooleanField()
    temporary = models.BooleanField()
    upload_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

class Alarm(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user_id = models.IntegerField()
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_id = models.ForeignKey(Like, on_delete=models.CASCADE)
    alarm_date = models.DateTimeField(auto_now_add=True)



class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add = True) # 생성 시간 
    updated_at = models.DateTimeField(auto_now = True)  # 수정 시간 




