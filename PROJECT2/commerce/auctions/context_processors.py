from django.conf import settings

def watchlist_count(request):
    if request.user.is_authenticated:
        return {
            'watchlist_count': request.user.watch_list.count()
        }
    return {
        'watchlist_count': 0
    }
