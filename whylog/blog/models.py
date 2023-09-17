from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField 

class Category(models.Model):
    category = models.CharField(max_length=50)

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = HTMLField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_img = models.TextField()
    in_private = models.BooleanField()
    temporary = models.BooleanField()
    upload_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_alarms')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user_alarms')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    alarm_date = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)



class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add = True) # 생성 시간 
    updated_at = models.DateTimeField(auto_now = True)  # 수정 시간 




