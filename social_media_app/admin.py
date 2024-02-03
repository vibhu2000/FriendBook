from django.contrib import admin
from .models import Blog, post, profile, Comment, UserStatus, FriendRequest, blog_Categorie

# Register your models here.

class PostCreated(admin.ModelAdmin):
    readonly_fields = ('created', )

class BlogCreated(admin.ModelAdmin):
    readonly_fields = ('blogCreated', )

admin.site.register(post, PostCreated)
admin.site.register(profile)
admin.site.register(Comment)
admin.site.register(UserStatus)
admin.site.register(FriendRequest)
admin.site.register(Blog, BlogCreated)
admin.site.register(blog_Categorie)