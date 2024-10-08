from django.contrib import admin
from .models import User, Category, Listing,Comment,Bid

# Register the User model
admin.site.register(User)

# Register the Listing model
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
# Register the Category model with a custom admin class
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'emoji')
    search_fields = ('category_name',)
