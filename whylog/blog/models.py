from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=50)

class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_login_date = models.DateTimeField()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_img = models.TextField()
    in_private = models.BooleanField()
    temporary = models.BooleanField()
    upload_date = models.DateTimeField()
    count = models.IntegerField()




