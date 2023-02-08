from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    
    def serialize(self):
        return {
            "user": self.user.username,
            "following": [user.username for user in self.following.all()]
        }
    def __str__(self):
        return f"{self.user.username} Profile"

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    likesNumber = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likesNumber": self.likesNumber
        }
    def __str__(self):
        return f"{self.user} posted at {self.timestamp}"