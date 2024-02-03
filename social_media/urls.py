"""social_media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from social_media_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.usersignup, name='usersignup'),
    path('signin/', views.usersignin, name='usersignin'),
    path('feed/', views.usersfeed, name='usersfeed'),
    path('status/<int:UserStatus_pk>', views.status_save, name='status_save'),
    path('like/', views.like_post, name='like_post'),
    path('search-users/', views.usersearch, name='usersearch'),
    path('search/', views.search, name='search'),
    path('logout/', views.logoutuser, name='userslogout'),
    path('savepost/', views.savepost, name='userpost'),
    path('comment/<int:pk>', views.commentpost, name='commentpost'),
    path('deletecomment/<int:comment_pk>/', views.deletecomment, name='usercommentdelete'),
    path('<int:post_pk>/deletepost/', views.deletepost, name='userpostdelete'),
    path('profile/<int:user_id>', views.userprofile, name='userprofile'),
    path('saveprofile/<int:profile_pk>', views.saveprofile, name='usersaveprofile'),
    path('settings/', views.editprofile, name='editprofile'),
    path('setprofile/', views.setprofile, name='setprofile'),
    path('savenewprofile/', views.savenewprofile, name='savenewprofile'),
    path('add-friend/<int:id>/',views.send_request,name='add-friend'),
    path('cancel-request/<int:id>/',views.cancel_request,name='cancel-request'),
    path('accept/<int:id>/',views.accept_request,name='accept'),
    path('ignore-request/<int:id>/',views.ignore_request,name='ignore-request'),
    path('remove-friend/<int:id>/',views.remove_friend,name='remove-friend'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('blogs/', views.blog, name='blog'),
    path('blog_detail/<int:pk>', views.blog_detail, name='blog_detail'),
    path('write-blog/', views.writeblog, name='writeblog'),
    path('blogs-create/', views.saveblog, name='saveblog'),
    path('my-blogs/', views.myBlogs, name='myBlogs'),
    path('edit-blog/<int:pk>', views.EditBlogs, name='blogedit'),
    path('update-blog/<int:pk>', views.updateblog, name='updateblog'),
    path('delete-blog/<int:pk>', views.deleteblog, name='deleteblog'),
    path('searchblog', views.blogsearch, name='searchblog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)