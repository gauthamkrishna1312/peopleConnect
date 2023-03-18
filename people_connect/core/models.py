from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.
User = get_user_model()
class Profiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimage = models.ImageField(upload_to='profile_images', default="default_profile.png")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
#for creating post in account
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
#for like a post
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username