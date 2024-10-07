from django.contrib import admin
from .models import User,Post,PostComment,Follow,Liked

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Follow)
admin.site.register(Liked)