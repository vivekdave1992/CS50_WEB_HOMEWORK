from django.conf import settings
from .models import Category

def watchlist_count(request):
    if request.user.is_authenticated:
        watchlist_count = request.user.watch_list.count()
    else:
        watchlist_count = 0
    
    # Get all categories
    allcategories = Category.objects.all()
    
    return {
        'watchlist_count': watchlist_count,
        'allcategories': allcategories
    }
