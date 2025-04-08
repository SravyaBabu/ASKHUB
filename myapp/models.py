from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime    
# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=20)
    usertype=models.CharField(max_length=20)
    viewPassword=models.CharField(max_length=200,null=True)

class User(models.Model):
    loginid = models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    photo=models.ImageField(upload_to="Image",null=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username=models.EmailField()
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=200)
    dob = models.DateField()
    bio = models.CharField(max_length=200)

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='questionimage', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    countanswers = models.IntegerField(default=0)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
