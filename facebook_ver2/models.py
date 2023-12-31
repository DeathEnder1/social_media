from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class Profiles(AbstractUser):
    first_name = models.CharField(max_length=200, blank= False)
    last_name =  models.CharField(max_length=200, blank= False)
    follows= models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    bio = models.TextField(default="No bio yet", max_length=300)
    email = models.EmailField(max_length=200)
    avatar = models.ImageField(default="avatar.svg")
    online_status = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    

    def get_blocking_users(self):
        return Profiles.objects.filter(blocker__blocked_user=self)


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profiles, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="posts")
    
    def num_comments(self):
        return self.comment_set.all().count()
    
    class Meta:
        ordering = ('-created',)
    

class Comment(models.Model):
    user = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body

class Block(models.Model):
    blocker = models.ForeignKey(Profiles, related_name='blocker', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(Profiles, related_name='blocked_user', on_delete=models.CASCADE)
    
LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,max_length=20)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.message