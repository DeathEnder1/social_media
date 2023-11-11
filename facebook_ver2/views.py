from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.db.models import Q
import pusher
from django.urls import reverse_lazy, reverse
def home(request):
    if request.user.is_authenticated:
        user = Profiles.objects.get(id=request.user.id)
        articles= Post.objects.all()
        blocked_users = Block.objects.filter(blocker=user).values_list('blocked_user', flat=True)
        articles= Post.objects.exclude(author__in=blocked_users)
        context = {
            'articles':articles
        }
        return render(request, 'home.html',context)
    else: 
        return redirect('/login')
    
def following(request):
    if request.user.is_authenticated:
        user = Profiles.objects.get(id=request.user.id)
        articles= Post.objects.all()
        follows = user.follows.all()
        context = {
            'articles':articles
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
        email = request.POST['email']
        checkemail = Profiles.objects.filter(email=email)
        if checkemail.count():
            messages.error(request, 'Email Already Exist')
        elif form.is_valid():
            form.save()
            return redirect('/user_page/'+str(uid))
    return render(request,'setting.html', {'form':form})

@login_required(login_url='login')
def user_page(request,id):
    user = Profiles.objects.get(id=id)   
    st = Post.objects.filter(author = id)
    postform =PostForm()
    commentform = CommentForm()
    p_add = False
    is_blocked = Block.objects.filter(blocker= request.user, blocked_user=Profiles.objects.get(id=id)).exists()
    if request.method == "POST" :
        aid = request.session.get('_auth_user_id')
        current_user = Profiles.objects.get(id=aid)

        if user in current_user.follows.all():
            current_user.follows.remove(user)
        else:
            current_user.follows.add(user)
        

    if "submit_postform" in request.POST:
        postform =PostForm(request.POST, request.FILES)
        if postform.is_valid(): 
            formin = postform.save(commit=False)
            formin.author = user
            formin.save()
            # postform = PostForm()
            p_add = True
            return redirect('/user_page/'+str(id))
        
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

        if search_type == 'username':
            profiles = Profiles.objects.filter(username__contains=searched)
            return render(request, 'search.html', {'searched': searched, 'search_type': search_type, 'profiles': profiles})
        elif search_type == 'post':
            posts = Post.objects.filter(content__contains=searched)
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

    uid = request.user.id

    user = Profiles.objects.get(id = uid)

    follows = user.follows.all()

    context = {'user':user,

               'follows':follows}

    return render(request,"chat_room.html",context)




@login_required(login_url='login')

def chat_details(request,id):

    uid = request.user.id

    user = Profiles.objects.get(id = uid)

    follows = user.follows.get(id=id)

    form = ChatMessageForm()

    chats = ChatMessage.objects.all()

    receive_chats = ChatMessage.objects.filter(msg_sender=follows,msg_receiver=user,seen=False)

    receive_chats.update(seen=True)

    receive_chats_json = [

        {"id": chat.id, "body": chat.body} for chat in receive_chats

    ]

    if request.method == "POST":

        form = ChatMessageForm(request.POST)




        if form.is_valid():

            chat_message = form.save(commit=False)

            chat_message.msg_sender = user

            chat_message.msg_receiver = follows

            chat_message.save()

            return redirect('chat_details',id =follows.id)




    context = {'follows':follows,

               'form':form,

               'user':user,

               'chats':chats,

               "receive_chats": json.dumps(receive_chats_json)}

    request.session['last_received_message'] = receive_chats.last().id if receive_chats.exists() else None

    return render(request,"chat_details.html",context)




@login_required(login_url='login')

def sent_messages(request,id):

    uid = request.user.id

    user = Profiles.objects.get(id = uid)

    follows = user.follows.get(id=id)

    data = json.loads(request.body)

    new_chat = data["msg"]

    new_chat_message = ChatMessage.objects.create(body = new_chat,msg_sender = user,msg_receiver = follows,seen = False)

    pusher_client = pusher.Pusher(

        app_id = "1695930",

        key = "62781415eb4ada65ca96",

        secret = "c41bf0167df3de120779",

        cluster = "ap1",

        ssl=True)

    pusher_client.trigger('my-channel', 'my-event', {'msg': new_chat_message.body})

    return JsonResponse(new_chat_message.body,safe=False)




@login_required(login_url='login')

def receive_messages(request,id):

    uid = request.user.id

    user = Profiles.objects.get(id = uid)

    follows = user.follows.get(id=id)

    chats = ChatMessage.objects.filter(msg_sender=follows,msg_receiver=user)

    last_received_message = request.session.get('last_received_message')

    arr = [{"id": chat.id, "body": chat.body} for chat in chats if chat.id != last_received_message]

    return JsonResponse(arr, safe=False)







@login_required(login_url='login')

def chat_notification(request):

    uid = request.user.id

    user = Profiles.objects.get(id = uid)

    follows = user.follows.all()

    arr = []

    for follow in follows:

        chats = ChatMessage.objects.filter(msg_sender_id=follow,msg_receiver=user,seen = False)

        arr.append(chats.count())

    return JsonResponse(arr,safe=False)

