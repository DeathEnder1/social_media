from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profiles(AbstractUser):
    first_name = models.CharField(max_length=200, blank= True)
    last_name =  models.CharField(max_length=200, blank= True)
    bio = models.TextField(default="no bio", max_length=300)
    email = models.EmailField(unique=True ,max_length=200, blank=True)
    avatar = models.ImageField(default="avatar.svg")

    REQUIRED_FIELDS = []