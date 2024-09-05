from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.listings_by_category, name='listings_by_category'),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('remove_multiple_from_watchlist/', views.remove_multiple_from_watchlist, name='remove_multiple_from_watchlist'),
]
