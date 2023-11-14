from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profiles)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Block)
admin.site.register(ChatModel)


