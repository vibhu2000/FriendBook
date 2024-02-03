from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import post, profile, Comment, UserStatus, FriendRequest, Blog, blog_Categorie
from .forms import BlogForm, PostForm, ProfileForm, UserForm, CommentForm, StatusForm
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def home(request):
    return render(request, 'social_media/home.html')

def usersignup(request):
    if request.method == 'GET':
        return render(request, 'social_media/usersignup.html')
    else:
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'social_media/usersignup.html', {'error':'Email already exists'})
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('setprofile')
            except IntegrityError:
                return render(request, 'social_media/usersignup.html', {'error':'User already exists'})

def usersignin(request):
    if request.method == 'GET':
        return render(request, 'social_media/usersignin.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'social_media/usersignin.html', {'errorsignin':'Invalid User/Password'})
        else:
            login(request, user)
            return redirect('usersfeed')

@login_required
def usersfeed(request):
    users = User.objects.all()
    posts = post.objects.filter(Q(user__in=request.user.profile.friend.all()) | Q(user=request.user)).order_by('-created')
    comments = Comment.objects.all()
    status_form = StatusForm(request.POST)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friends = request.user.profile.friend.all()
    Hasliked = []
    Hasnotliked = []
    empty = []
    Notempty = []
    for i in posts:
        likes = i.like.all()
        for like in likes:
            if i.like.filter(id=request.user.id).exists():
                Hasliked.append(i.id)
            else:
                Hasnotliked.append(i.id)
        if Hasliked == []:
            empty.append(i.id)
        else: 
            Notempty.append(i.id)
    context = {
        'Post':posts,
        'User':users,
        'form':PostForm(),
        'Profile':profile,
        'Form':CommentForm(),
        'Comment':comments,
        'Status':status_form,
        'fr':friend_requests,
        'friend':friends,
        'Hasliked':Hasliked,
        'Hasnotliked':Hasnotliked,
        'empty':empty,
        'Notempty':Notempty,
    }
    return render(request, 'social_media/feed.html', context=context)

@login_required
def status_save(request,UserStatus_pk):
    if request.method == 'POST':
        y=get_object_or_404(UserStatus, pk=UserStatus_pk)
        status = StatusForm(request.POST, instance=y)
        if status.is_valid():
            Status=status.save(commit=False)
            Status.user=request.user
            Status.save()
        return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def like_post(request):
    Post = get_object_or_404(post, id=request.GET.get('post_id'))
    cssClass = 'colorRed'
    if Post.like.filter(id=request.user.id).exists():
        Post.like.remove(request.user)
    else:
        Post.like.add(request.user)
    count = Post.like.count()
    users = Post.like.all() 
    user = []
    for i in users:
        user.append((i.username))
    response = {
        'count':count,
        'users':user,
        'cssClass':cssClass,
    }
    return JsonResponse(response)

@login_required
def usersearch(request):
    qur = request.GET.get('search')
    u = User.objects.filter(username__contains = qur)
    user = User.objects.all()
    friend = request.user.profile.friend.all()
    if u:
        return render(request, 'social_media/search.html', {'User':user,'User_search':u,'Profile':profile,'friend':friend})
    else:
        return render(request, 'social_media/search.html', {'User':user,'Error':'No users found! :(','friend':friend})

@login_required
def search(request):
    if 'term' in request.GET:
        qs = User.objects.filter(username__contains=request.GET.get('term'))
        users = list()
        for i in qs:
            users.append(i.username)
        return JsonResponse(users, safe=False)

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('usersignin')

@login_required
def savepost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
            return redirect('usersfeed')

@login_required
def commentpost(request, pk):
    Post = get_object_or_404(post, pk=pk)
    comment = request.POST.get('comment')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.post = Post
            Form.comment = comment
            Form.user = request.user
            Form.save()
            return redirect('usersfeed') #Returns me to the same page/back to that page

@login_required
def deletecomment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user or comment.post.user.username:
        if request.method == 'GET':
            comment.delete()
            return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def deletepost(request, post_pk):
    Post = get_object_or_404(post, pk=post_pk, user=request.user)
    if request.method == 'GET':
        Post.delete()
        return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def userprofile(request, user_id=None):
    u=User.objects.all()
    user = get_object_or_404(User, id=user_id)
    sent_request = FriendRequest.objects.filter(from_user=request.user, to_user=user)
    if request.user.friended.filter(user=user):
        button_status = True
    else:
        button_status = False
    friends = user.friended.all()
    friend = request.user.profile.friend.all()
    if user:
        user = User.objects.get(id=user_id)
        Post = post.objects.order_by('-created')
    Hasliked = []
    Hasnotliked = []
    empty = []
    Notempty = []
    for i in Post:
        likes = i.like.all()
        for like in likes:
            if i.like.filter(id=request.user.id).exists():
                Hasliked.append(i.id)
            else:
                Hasnotliked.append(i.id)
        if Hasliked == []:
            empty.append(i.id)
        else: 
            Notempty.append(i.id)
    context = {
        'Post':Post,
        'User':user,
        'u':u,
        'button_status':button_status,
        'sent_request':sent_request,
        'friends':friends,
        'friend':friend,
        'Hasliked':Hasliked,
        'Hasnotliked':Hasnotliked,
        'empty':empty,
        'Notempty':Notempty,
    }
    return render(request,'social_media/profile.html', context=context)

@login_required
def saveprofile(request,profile_pk):
    if request.method == 'POST':
        y = get_object_or_404(profile, pk=profile_pk, user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=y)
        form2 = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
        if form2.is_valid():
            form2.save()
        return redirect(request.META['HTTP_REFERER']) 

@login_required
def editprofile(request):
    form = ProfileForm(instance=request.user.profile)
    form2 = UserForm(instance=request.user)
    return render(request, 'social_media/settings.html', {'Form':form,'Form2':form2})

@login_required
def savenewprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form2 = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
        if form2.is_valid():
            form2.save()
        return redirect('usersfeed')

@login_required
def setprofile(request):
    form = ProfileForm(request.POST,request.FILES)
    form2 = UserForm(request.POST)
    return render(request, 'social_media/setprofile.html', {'Form':form,'Form2':form2})

@login_required
def send_request(request,id):
    from_user=request.user
    to_user=User.objects.get(id=id)
    freq=FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def cancel_request(request,id):
    user1=request.user
    user2=User.objects.get(id=id)
    freq = FriendRequest.objects.filter(from_user=user1,to_user=user2)
    freq.delete()
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def accept_request(request,id):
    freq=FriendRequest.objects.get(id=id)
    user1=request.user
    user2=freq.from_user
    user1.profile.friend.add(user2)
    user2.profile.friend.add(user1)
    freq.delete()
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def ignore_request(request,id):
    freq=FriendRequest.objects.get(id=id)
    user1=request.user
    user2=freq.from_user
    freq.delete()
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def remove_friend(request,id):
    user1=request.user
    user2=User.objects.get(id=id)
    user1.profile.friend.remove(user2)
    user2.profile.friend.remove(user1)
    return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def room(request, room_name):
    user = User.objects.all()
    friend = request.user.profile.friend.all()
    context = {
        'room_name': room_name,
        'User':user,
        'friend':friend
    }
    return render(request, 'social_media/room.html', context=context)

@login_required
def blog(request):
    users = User.objects.all()
    status_form = StatusForm(request.POST)
    friends = request.user.profile.friend.all()
    blogs = Blog.objects.all()
    context = {
        'User':users,
        'friend':friends,
        'Status':status_form,
        'blogs':blogs,
    }
    return render(request, 'social_media/blog.html', context=context)

@login_required
def blog_detail(request,pk):
    blog = get_object_or_404(Blog, pk=pk)
    users = User.objects.all()
    status_form = StatusForm(request.POST)
    friends = request.user.profile.friend.all()
    context = {
        'blog':blog,        
        'User':users,
        'friend':friends,
        'Status':status_form,
    }
    return render(request, 'social_media/blog_detail.html', context=context)

from pprint import pprint

@login_required
def writeblog(request):
    Blog_Categories = blog_Categorie.objects.all()
    users = User.objects.all()
    status_form = StatusForm(request.POST)
    friends = request.user.profile.friend.all()
    context = {
        'User':users,
        'friend':friends,
        'Status':status_form,
        'Categories':Blog_Categories,
        'blogForm':BlogForm(),
    }
    return render(request, 'social_media/blog_create.html', context=context)

@login_required
def saveblog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.blogUser = request.user
            Form.save()
            return redirect('myBlogs')
        else:
            context = {
                'error':'Please provide Valid data!',
            }
            return render(request, 'social_media/blog_create.html', context=context)

@login_required
def myBlogs(request):
    blogs = Blog.objects.filter(blogUser=request.user.id)
    context = {
        'blogs':blogs,
    }
    return render(request, 'social_media/userOwnBlogs.html', context=context)

@login_required
def EditBlogs(request,pk):
    blog = Blog.objects.get(id=pk)
    Blog_Categories = blog_Categorie.objects.all()
    users = User.objects.all()
    status_form = StatusForm(request.POST)
    friends = request.user.profile.friend.all()
    context = {
        'User':users,
        'friend':friends,
        'Status':status_form,
        'Categories':Blog_Categories,
        'blog':blog,
    }
    return render(request, 'social_media/blog_edit.html', context=context)

@login_required
def updateblog(request,pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.blogUser = request.user
            Form.save()
            return redirect('myBlogs')
        else:
            pprint(form.errors)
            return HttpResponse(form.errors)

@login_required
def deleteblog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user == blog.blogUser:
        blog.delete()
        return redirect(request.META['HTTP_REFERER']) #Returns me to the same page/back to that page

@login_required
def blogsearch(request):
    qur = request.GET.get('search')
    u = Blog.objects.filter(blogTitle__contains = qur)
    user = User.objects.all()
    friend = request.user.profile.friend.all()
    context = {
        'User':user,
        'User_search':u,
        'Profile':profile,
        'friend':friend,
        'Error':'No blogs found! :('
    }
    if u:
        return render(request, 'social_media/blog.html', context=context)
    else:
        return render(request, 'social_media/blog.html', context=context)