from django.contrib import admin
from .models import Profiles,Post,Comment,Like
# Register your models here.

admin.site.register(Profiles)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)