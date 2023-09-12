from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    category = models.CharField(max_length=50)

class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_login_date = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100, default = None)

class Blog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True,null=True)
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







