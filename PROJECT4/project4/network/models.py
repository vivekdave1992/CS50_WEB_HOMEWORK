from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Remove the ManyToManyField, as the Follow model will handle the relationships
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "followers": [user.follower.username for user in self.follower_set.all()],  # List of followers using the Follow model
            "following": [user.following.username for user in self.following_set.all()]  # List of users being followed using the Follow model
        }

    def __str__(self):
        return f"User {self.username} with {self.follower_set.count()} followers"


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


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_following')
        ]

    def save(self, *args, **kwargs):
        # Prevent a user from following themselves
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

