from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watch_list = models.ManyToManyField("Listing",blank=True,  related_name='watched_by')
class Category(models.Model):
    category_name = models.CharField(max_length=64)
    emoji = models.CharField(max_length=10, blank=True, null=True)  # Add this line

    def __str__(self):
        return f"{self.category_name} {self.emoji}"
    

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)  # Increased length for detailed descriptions
    image_url = models.CharField(max_length=1000 ,blank=True, null=True)
    status = models.BooleanField(default=True)  # Assuming default status is active
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="user")
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically adds current date and time
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Proper field for currency
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,related_name="listing_category")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="buyer")

    def __str__(self):
        return f"{self.title} : {self.status}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True,related_name="listingComment")
    comment_time = models.DateTimeField(auto_now_add=True)  # Automatically adds current date and time
    message = models.CharField(max_length=200)
    objects = models.Manager()
    
    
    def __str__(self) -> str:
        return f"{self.author} commented on {self.listing}  at {self.comment_time}"
    

