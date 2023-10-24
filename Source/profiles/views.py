from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from Posts.models import Post
from Posts.forms import PostForm
# Create your views here.
def my_profile_view(request):
    confirm = False
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    postform =PostForm(request.POST or None, request.FILES or None)
    p_add = False

    if "submit_postform" in request.POST:
        postform =PostForm(request.POST, request.FILES)
        if postform.is_valid():
            formin = postform.save(commit=False)
            formin.author = profile
            formin.save()
            postform = PostForm()
            p_add = True

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True
            
    context={
        'profile':profile,
        'form':form,
        'confirm':confirm,
        'postform':postform,
        'p_add':p_add
    }
    return render(request,'profiles/myprofile.html', context)



