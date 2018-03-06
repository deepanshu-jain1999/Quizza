from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True)


class Quiz(models.Model):
    category = models.CharField(max_length=200)
    question = models.TextField(max_length=1000)
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.id


