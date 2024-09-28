from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "followers": [user.username for user in self.followers.all()],  # List of followers
            "following": [user.username for user in self.following.all()]   # List of users being followed
        }

    def __str__(self):
        return f"User {self.username} with {self.followers.count()} followers"


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="post_user")
    post_content = models.CharField(max_length=512)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username if self.poster else None,
            "post_content": self.post_content,
            "date_added": self.date_added.strftime("%d %b %Y, %H:%M %S"),
            "last_updated": self.last_updated.strftime("%d %b %Y, %H:%M %S"),
            "likes": self.likes,
            "comments": [comment.serialize() for comment in self.post_comment.all()]  # Serializing related comments
        }

    def __str__(self):
        return f"Post {self.id} by {self.poster} at {self.date_added}"


class PostComment(models.Model):  # Changed to 'PostComment' for better clarity
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post_comment")
    comment_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=512)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username if self.author else None,
            "post": self.post.id if self.post else None,
            "comment_time": self.comment_time.strftime("%b %d %Y, %I:%M %p"),
            "message": self.message
        }

    def __str__(self):
        return f"{self.author} commented on Post {self.post.id} at {self.comment_time}"
