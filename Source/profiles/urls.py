from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('myprofile/',my_profile_view,name='my_profile_view'),
]