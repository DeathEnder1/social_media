from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Block, Profiles,Post,Comment,Like
from .forms import BlockForm, Profile_Form,MyUserCreationForm,PostForm,CommentForm
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        blocked_users = Block.objects.filter(blocker=current_user).values_list('blocked_user', flat=True)
        articles= Post.objects.exclude(author__in=blocked_users)
        context = {
        'articles':articles
        }
        return render(request, 'main/home.html',context)
    else:
        return redirect('login/')

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
    is_blocked = Block.objects.filter(blocker= request.user, blocked_user=Profiles.objects.get(id=id)).exists()
    
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
            
    
    context={
            'user':user,
             'st':st,
             'postform':postform,
             'commentform ':commentform ,
             'p_add':p_add,
             'profile_user': request.user,
             'is_blocked': is_blocked,
            }

    return render(request,'user_page.html',context)

    

@login_required(login_url='login')
def block_user(request, id):
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            blocker = request.user
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
#def search(request):
#	if request.method == "POST":
#     
#		searched= request.POST['searched']
#		profile = Profiles.objects.filter(username__contains=searched)
#	
#		return render(request, 
#		'search.html', 
#		{'searched':searched,
#		'profile':profile})
#	else:
#		return render(request, 
#		'search', {})

#def search(request):
#    if request.method == "POST":
#        searched = request.POST['searched']
#        search_type = request.POST.get('search_type', 'username')  # Sử dụng 'username' mặc định nếu không có giá trị được chọn
#
#        if search_type == 'username':
#            profiles = Profiles.objects.filter(username__contains=searched)
#            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'profiles': profiles})
#        elif search_type == 'post':
#            posts = Post.objects.filter(content__contains=searched)
#            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'posts': posts})
#    else:
#        return render(request, 'search.html', {})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        search_type = request.POST.get('search_type', 'username')  

        blocked_users = request.user.get_blocked_users()

        if search_type == 'username':
            profiles = Profiles.objects.filter(username__contains=searched).exclude(id__in=blocked_users)
            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'profiles': profiles})
        elif search_type == 'post':
            posts = Post.objects.filter(content__contains=searched, author__in=blocked_users)
            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'posts': posts})
    else:
        return render(request, 'search.html', {})