from django.urls import path
from .views import *

app_name = 'Posts'

urlpatterns = [
    path('',post_comment_list, name='post_comment_list'),
    path('liked/',like_unlike_posts,name='like_unlike_posts'),
]