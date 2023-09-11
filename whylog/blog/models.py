from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=50)

class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_login_date = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category)
    blog_img = models.TextField()
    in_private = models.BooleanField()
    temporary = models.BooleanField()
    upload_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()

class Comment(models.Model):
    user_id = models.ForeignKey(User)
    comment = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user_id = models.ForeignKey(User)
    blog_id = models.ForeignKey(Blog)
    comment_id = models.ForeignKey(Comment)
    upload_date = models.DateTimeField(auto_now_add=True)

class Alarm(models.Model):
    user_id = models.IntegerField()
    target_user_id = models.IntegerField()
    blog_id = models.ForeignKey(Blog)
    comment_id = models.ForeignKey(Comment)
    like_id = models.ForeignKey(Like)
    alarm_date = models.DateTimeField(auto_now_add=True)







