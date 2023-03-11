from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Built in Django user model, we save username, email, password here
User = get_user_model()

# user should have a “home” page that shows their user information and any other interesting data such as images, picture galleries or other media files. 
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default="profile_images/profile-picture-placeholder.png")
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

# R1 f) Users can add status updates to their home page
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=256, blank=True)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class PostLikes(models.Model):
    post_id = models.CharField(max_length=256)
    username = models.CharField(max_length=256)

    def __str__(self):
        return self.username
        
# R1 d) Users can add other users as friends
class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower