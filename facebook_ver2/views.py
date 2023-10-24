from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profiles
from .forms import Profile_Form,MyUserCreationForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def login_page(request):
    page='login'
    if request.user.is_authenticated:
       return redirect('/') 
    
    if request.method=="POST":
        usern=request.POST.get('Username', '')
        passw =request.POST.get('Password', '')
        
        user=authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,"Username or Password does NOT exist")
    return render(request, 'login_register.html', {'page':page})

def register(request):
    form = MyUserCreationForm()
    if request.method=='POST':  
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('/')
        else: 
            messages.error(request, 'Something went wrong please try again.')
    return render(request, 'login_register.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def profile(request):
    uid=request.session.get('_auth_user_id')
    user =Profiles.objects.get(id=uid)
    context={'user':user}
    return render(request,'profile.html')

@login_required(login_url='login')
def setting(request):
    uid=request.session.get('_auth_user_id')
    user =Profiles.objects.get(id=uid)
    context={'user':user}
    form=Profile_Form(instance=user)
    if request.method=="POST":
        form=Profile_Form(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("/profile")
    return render(request,'setting.html', {'form':form})