from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Profiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimage = models.ImageField(upload_to='profile_images', default="default_profile.png")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
