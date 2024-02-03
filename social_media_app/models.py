from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.signals import post_save

# Create your models here.

class post(models.Model):
    user = models.ForeignKey(User,default='' , related_name='has_liked', on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, null=True, blank=True, default=0)

    def __str__(self):
        return self.caption

    def total_likes(self):
        return self.like.count()

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    desc = models.TextField(null=True)
    pfp = models.ImageField(default='profile.png', upload_to='profile_pics/', null=True, blank=True)
    cover = models.ImageField(default='cover.png', upload_to='cover_pics/', null=True, blank=True)
    occupation = models.CharField(max_length=250, default='')
    friend = models.ManyToManyField(User, blank=True, null=True, related_name='friended')

    def __str__(self):
        return self.user.username

    def create_profile(sender,instance,created,**kwargs):
        if created:
            profile.objects.create(user=instance)

    post_save.connect(create_profile, sender=User)

class UserStatus(models.Model):
    status = models.CharField(max_length=50, default='Available', null=True, blank=True, editable=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')

    def __str__(self):
        return self.user.username

    def create_status(sender,instance,created,**kwargs):
        if created:
            UserStatus.objects.create(user=instance)

    post_save.connect(create_status, sender=User)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null=True)
    post = models.ForeignKey(post, related_name='Comment', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.comment

class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True) # set when created

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class blog_Categorie(models.Model):
    categoryTitle = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryTitle

class Blog(models.Model):
    blogTitle = models.CharField(max_length=100)
    blogContent = models.TextField()
    blogUser = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    blogCreated = models.DateField(null=True, blank=True,auto_now_add=True)
    blogImgOne = models.ImageField(upload_to='Blogimages/', default='')
    blogCategory = models.ForeignKey(blog_Categorie, on_delete=models.CASCADE, default='')

    def __str__(self):
        return str(str(self.blogTitle)  + ' - ' + str(self.blogUser))