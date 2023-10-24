from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    user = request.user
    hello = "Djt Me may"
    context =  {
        'user':user,
        'hello':hello,
    }
    return render(request,'main/home.html',context)