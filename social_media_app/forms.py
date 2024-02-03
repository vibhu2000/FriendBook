from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from .models import Blog, post, profile, Comment, UserStatus

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['caption','image','video']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['desc','pfp','cover','occupation']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class StatusForm(forms.ModelForm):
    class Meta:
        model = UserStatus
        fields = ['status']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['blogTitle','blogContent','blogCategory','blogImgOne']