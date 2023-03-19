from django.contrib import admin
from .models import Profiles, Post, LikePost, FollowersCount


# Register your models here.

admin.site.register(Profiles)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)