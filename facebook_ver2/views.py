from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profiles,Post,Comment,Like
from .forms import Profile_Form,MyUserCreationForm,PostForm,CommentForm
from django.http import HttpResponse

# Create your views here.

def home(request):
    articles= Post.objects.all()
    context = {
        'articles':articles
    }
    return render(request, 'main/home.html',context)

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
    st = Post.objects.filter(author = uid)
    user = Profiles.objects.get(id=uid)
    postform =PostForm()
    commentform = CommentForm()
    p_add = False

    if "submit_postform" in request.POST:
        postform =PostForm(request.POST, request.FILES)
        if postform.is_valid(): 
            formin = postform.save(commit=False)
            formin.author = user
            formin.save()
            # postform = PostForm()
            p_add = True
            return redirect("/profile") 
        
    if "submit_commentform" in request.POST:
        commentform = CommentForm(data=request.POST)
        if commentform.is_valid():
            formin = commentform.save(commit=False)
            formin.user = user
            formin.post = Post.objects.get(id=request.POST.get('post_id'))
            # commentform = CommentForm()
            formin.save()
            
    
    context={'user':user,
             'st':st,
             'postform':postform,
             'commentform ':commentform ,
             'p_add':p_add,}
    
    return render(request,'profile.html',context)

@login_required(login_url='login')
def delete(request, id):
    st=Post.objects.get(id=id)
    if request.method=='POST':
        if request.user== st.author:
            st.delete()
            return redirect('/profile')
        else:
            return HttpResponse('You can not edit this post')
    return render(request, 'delete.html', {'st':st})

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

@login_required(login_url='login')
def user_page(request,id):
    user = Profiles.objects.get(id=id)
    st = Post.objects.filter(author = id)
    postform =PostForm()
    commentform = CommentForm()
    p_add = False

    if "submit_postform" in request.POST:
        postform =PostForm(request.POST, request.FILES)
        if postform.is_valid(): 
            formin = postform.save(commit=False)
            formin.author = user
            formin.save()
            # postform = PostForm()
            p_add = True
            return redirect("/profile") 
        
    if "submit_commentform" in request.POST:
        commentform = CommentForm(data=request.POST)
        if commentform.is_valid():
            formin = commentform.save(commit=False)
            formin.user = user
            formin.post = Post.objects.get(id=request.POST.get('post_id'))
            # commentform = CommentForm()
            formin.save()
            
    
    context={'user':user,
             'st':st,
             'postform':postform,
             'commentform ':commentform ,
             'p_add':p_add,}

    return render(request,'user_page.html',context)

@login_required(login_url='login')
def block_user(request, id):
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            blocker = request.user
            blocked_user = User.objects.get(id=id)
            if form.cleaned_data['action'] == 'block':
                Block.objects.create(blocker=blocker, blocked_user=blocked_user)
            else:
                Block.objects.filter(blocker=blocker, blocked_user=blocked_user).delete()
            return redirect('profile', user_id=id)
    return redirect('')