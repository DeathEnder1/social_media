from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.db.models import Q

from django.urls import reverse_lazy, reverse
def home(request):
    if request.user.is_authenticated:
        postform =PostForm()
        commentform=CommentForm()
        user = Profiles.objects.get(id=request.user.id)
        items = list(Profiles.objects.all())
        alluser = random.sample(items, 1)
        blocked_users = Block.objects.filter(blocker=user).values_list('blocked_user', flat=True)
        blocker = Block.objects.filter(blocked_user=request.user).values_list('blocker', flat=True)
        articles = Post.objects.exclude(Q(author__in=blocked_users) | Q(author__in=blocker))

        if request.method == "POST" :
            if "submit_postform" in request.POST:
                postform =PostForm(request.POST, request.FILES)
                if postform.is_valid(): 
                    formin = postform.save(commit=False)
                    formin.author = user
                    formin.save()
                    # postform = PostForm()
                    p_add = True
                    return redirect('/')
            
            elif "submit_commentform" in request.POST:
                commentform = CommentForm(request.POST)
                if commentform.is_valid():
                    formin = commentform.save(commit=False)
                    formin.user = Profiles.objects.get(id = request.user.id)
                    formin.post = Post.objects.get(id=request.POST.get('post_id'))
                    formin.save()
                response_data = {
                    'comment': {
                        'user': formin.user.username,
                        'body': formin.body,
                        }
                    }
                return(redirect('/'))
                # return JsonResponse(response_data)

        context = {
            'articles':articles,
            'postform':postform,
            'alluser' : alluser,
        }
        return render(request, 'home.html',context)
    else: 
        return redirect('/login')
    
def following(request):
    if request.user.is_authenticated:
        user = Profiles.objects.get(id=request.user.id)
        articles= Post.objects.all()
        follows = user.follows.all()
        commentform=CommentForm()
        if request.method == "POST" :
            if "submit_commentform" in request.POST:
                commentform = CommentForm(request.POST)
                if commentform.is_valid():
                    formin = commentform.save(commit=False)
                    formin.user = Profiles.objects.get(id = request.user.id)
                    formin.post = Post.objects.get(id=request.POST.get('post_id'))
                    formin.save()
                response_data = {
                    'comment': {
                        'user': formin.user.username,
                        'body': formin.body,
                        }
                    }
                return(redirect('/following'))
        context = {
            'articles':articles,
            'follows':follows,
            'commentform':commentform,
        }
        return render(request, 'following.html',context)
    else: 
        return redirect('/login')

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
    password1 = request.POST.get('password1',False)
    password2 = request.POST.get('password2',False)
    username = request.POST.get('username',False)
    checkusername = Profiles.objects.filter(username=username)
    if request.method=='POST':  
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('/')
        elif(password1 != password2): 
            messages.error(request, 'Passwords do not match')
        elif checkusername.count():
            messages.error(request, 'User Already Exist')
        else:
            messages.error(request, 'Password must at least 8 charaters')
    return render(request, 'login_register.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def delete(request, id):
    st=Post.objects.get(id=id)
    uid=request.session.get('_auth_user_id')
    if request.method=='POST':
        if request.user== st.author:
            st.delete()
            return redirect('/user_page/'+str(uid))
        else:
            return HttpResponse('You can not delete this post')
    return render(request, 'delete.html', {'st':st})

@login_required(login_url='login')
def update(request, id):
    st=Post.objects.get(id=id)
    form =PostForm(instance=st)
    uid=request.session.get('_auth_user_id')
    if request.method=='POST':
        form = PostForm(request.POST,request.FILES,instance=st)
        if form.is_valid():
            form.save()
            return redirect('/user_page/'+str(uid))
        else:
            return HttpResponse('You can not edit this post')
    else:
        form = PostForm(instance=st)
    return render(request, 'update.html',{'form':form})
        

@login_required(login_url='login')
def setting(request):
    uid=request.session.get('_auth_user_id')
    user =Profiles.objects.get(id=uid)
    context={'user':user}
    form=Profile_Form(instance=user)
    if request.method=="POST":
        form=Profile_Form(request.POST, request.FILES,instance=user)
        email_form = request.POST['email']
        checkemail = Profiles.objects.filter(email=email_form)
        if checkemail.count() and user.email != email_form:
            messages.error(request, 'Email Already Exist')
        elif form.is_valid():
            form.save()
            return redirect('/user_page/'+str(uid))
    return render(request,'setting.html', {'form':form})

@login_required(login_url='login')
def user_page(request,id):
    user = Profiles.objects.get(id=id)   
    # user2 = Profiles.objects.get(id = request.user.id)
    st = Post.objects.filter(author = id)
    postform =PostForm()
    commentform = CommentForm()
    p_add = False
    is_blocked = Block.objects.filter(blocker= request.user, blocked_user=Profiles.objects.get(id=id)).exists()
    if request.method == "POST" :
        if "submit_postform" in request.POST:
            postform =PostForm(request.POST, request.FILES)
            if postform.is_valid(): 
                formin = postform.save(commit=False)
                formin.author = user
                formin.save()
                # postform = PostForm()
                p_add = True
                return redirect('/user_page/'+str(id))
        
        elif "submit_commentform" in request.POST:
            commentform = CommentForm(data=request.POST)
            if commentform.is_valid():
                formin = commentform.save(commit=False)
                formin.user = user
                formin.post = Post.objects.get(id=request.POST.get('post_id'))
                # commentform = CommentForm()
                formin.save()
            return(redirect('/user_page/{{request.user.id}}'))

        else:     
            aid = request.session.get('_auth_user_id')
            current_user = Profiles.objects.get(id=aid)

            if user in current_user.follows.all():
                current_user.follows.remove(user)
            else:
                current_user.follows.add(user)
            
    
    context={'user':user,
             'st':st,
             'postform':postform,
             'commentform ':commentform ,
             'p_add':p_add,
             'is_blocked':is_blocked
             }

    return render(request,'user_page.html',context)

@login_required(login_url='login')
def block_user(request, id):
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            aid = request.session.get('_auth_user_id')
            blocker = Profiles.objects.get(id=aid)
            follows = blocker.follows.all()
            blocked_user = Profiles.objects.get(id=id)  # Lấy thông tin người bị block từ id truyền vào
            action = form.cleaned_data['action']
            if action == 'block':
                # Kiểm tra xem có sẵn một bản ghi block hay không
                existing_block = Block.objects.filter(blocker=blocker, blocked_user=blocked_user).first()
                if not existing_block:
                    Block.objects.create(blocker=blocker, blocked_user=blocked_user)
            elif action == 'unblock':
                Block.objects.filter(blocker=blocker, blocked_user=blocked_user).delete()
            return redirect('/', user_id=id)
    return redirect('')

@login_required(login_url='login')
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        search_type = request.POST.get('search_type', 'username')  # Sử dụng 'username' mặc định nếu không có giá trị được chọn

        blocking_users = request.user.get_blocking_users()

        if search_type == 'username':
            profiles = Profiles.objects.filter(username__contains=searched).exclude(id__in=blocking_users)
            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'profiles': profiles})
        elif search_type == 'post':
            posts = Post.objects.filter(content__contains=searched).exclude(author__in=blocking_users)
            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'posts': posts})
    else:
        return render(request, 'search.html', {})
    
@csrf_exempt
@login_required(login_url='login')
def like_unlike_post(request):
    user =request.user.id
    if request.method=="POST":
        post_id= request.POST.get('post_id')
        post= Post.objects.get(id=post_id)
        profile= Profiles.objects.get(id=user)
        if profile in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        like, created= Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else: 
                like.value='Like'
        else:
            like.value='Like'
            post.save()
            like.save()
        data ={
            'value': like.value,
            'likes': post.liked.all().count()
        }
        
        return JsonResponse(data, safe=False)
    
    return redirect('/')

@login_required(login_url='login')
def chat_room(request):
    users = Profiles.objects.exclude(username = request.user.username)
    context = {
        'users':users,
    }
    return render(request, 'chat_room.html',context)

@login_required(login_url='login')
def chat_page(request,username):
    user_obj = Profiles.objects.get(username=username)
    users = Profiles.objects.exclude(username = request.user.username)
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_obj = ChatModel.objects.filter(thread_name=thread_name)
    context = {
        'users': users,
        'user': user_obj,
        'messages':message_obj
    }
    return render(request, 'chat_page.html',context)
