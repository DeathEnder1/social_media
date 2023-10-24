from django.shortcuts import render,redirect
from .models import Post,Like
from profiles.models import Profile
from .forms import PostForm,CommentForm
# Create your views here.

def post_comment_list(request):
    st = Post.objects.all()
    profile = Profile.objects.get(user = request.user)
    postform =PostForm()
    commentform = CommentForm()
    p_add = False

    if "submit_postform" in request.POST:
        print(request.POST)
        postform =PostForm(request.POST, request.FILES)
        if postform.is_valid():
            formin = postform.save(commit=False)
            formin.author = profile
            formin.save()
            postform = PostForm()
            p_add = True
    
    if "submit_commentform" in request.POST:
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            formin = commentform.save(commit=False)
            formin.user = profile
            formin.post = Post.objects.get(id=request.POST.get('post_id'))
            formin.save()
            commentform = CommentForm()

    context = {
        'st':st,
        'profile':profile,
        'postform':postform,
        'commentform':commentform,
        'p_add':p_add,
    }
    return render(request,'Posts/main.html',context)

def like_unlike_posts(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            
            post_obj.save()
            like.save()
    return redirect('Posts:post_comment_list')
    