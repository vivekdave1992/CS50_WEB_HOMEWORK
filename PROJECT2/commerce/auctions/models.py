from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Catagory(models.Model):
    catagory_name = models.CharField(max_length=64)
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)  # Increased length for detailed descriptions
    image_url = models.CharField(max_length=1000)
    status = models.BooleanField(default=True)  # Assuming default status is active
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="user")
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically adds current date and time
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Proper field for currency
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE, blank=True, null=True,related_name="catagory")
    
    
