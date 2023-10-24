from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Nothing", max_length=200)
    email = models.EmailField(max_length=100,blank=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars/')
    # pip pillow
    slug = models.SlugField(unique=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def count_posts(self):
        return self.posts.all().count()
    
    def get_authors_posts(self):
        return self.posts.all()
    
    def given_likes(self):
        likes = self.like_set.all()
        total_liked = 0
        for i in likes:
            if i.value == 'Like':
                total_liked += 1
        return total_liked
    
    def receive_likes(self):
        posts = self.posts.all()
        total_liked = 0
        for i in posts:
            total_liked += i.liked.all().count()
        return total_liked

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name)+ " " + str(self.last_name))
            ex = Profile.objects.filter(slug = to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug = to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)