from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.

class Profiles(models.Model):
    first_name = models.CharField(max_length=200, blank= True)
    last_name =  models.CharField(max_length=200, blank= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio", max_length=300)
    email = models.EmailField(unique=True ,max_length=200, blank=True)
    avatar = models.ImageField(default="avatar.png", upload_to="avatars/")

    def str(self):
        return f"{self.user.username}"

    class Meta:
        db_table = 'Profiles'