from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
    # path('categories/', views.category_list, name='category_list'),
    # path('categories/<int:category_id>/', views.listings_by_category, name='listings_by_category'),
]
