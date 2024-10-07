from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User,Post,PostComment,Follow,Liked
import json

def index(request):
    all_post = Post.objects.all().order_by('last_updated').reverse()
    user_liked = []

    # Get the post IDs the user has liked
    if request.user.is_authenticated:
        user_like = Liked.objects.filter(user=request.user).values_list('post_id', flat=True)
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    post_of_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "all_post": all_post,
        "post_of_page": post_of_page,
        "user_like": list(user_like)  # Convert to list
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")  # Using .get() to avoid KeyError
        if content:  # Ensure that content is not empty
            user = User.objects.get(pk=request.user.id)
            post = Post(post_content=content, poster=user)
            post.save()
            return HttpResponseRedirect(reverse('index'))  # Assuming 'index' is your URL pattern name
        else:
            # You can handle the case where content is empty here
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))  # If request is not POST


def profile(request,user_id):
    profile_user = User.objects.get(pk=user_id)
    all_post= Post.objects.filter(poster=profile_user).order_by('last_updated').reverse()
    followers = Follow.objects.filter(following=profile_user)
    following = Follow.objects.filter(follower=profile_user)
    current_user =  User.objects.get(pk= request.user.id)
    isFollowing = False
    if request.user.is_authenticated:
        isFollowing = followers.filter(follower=current_user).exists()
        
    paginator = Paginator(all_post,10)
    page_number = request.GET.get('page')
    post_of_page = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{
        "all_post":all_post,
        "post_of_page":post_of_page,
        "profile_user":profile_user,
        "followers":followers,
        "following":following,
        "isFollowing": isFollowing,
    })

def follow_toggle(request):
    # Get the profile user id from the POST request
    profile_user_id = request.POST.get('profile_user')
    profile_user = User.objects.get(pk=profile_user_id)
    current_user = User.objects.get(pk=request.user.id)
    
    # Check if the current user is already following the profile user
    follow_relationship = Follow.objects.filter(follower=current_user, following=profile_user)
    
    if follow_relationship.exists():
        # Unfollow if already following
        follow_relationship.delete()
    else:
        # Follow if not already following
        Follow.objects.create(follower=current_user, following=profile_user)
    
    # Redirect back to the profile page
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': profile_user.id}))


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    
    # Get a list of users the current user is following
    following_users = Follow.objects.filter(follower=current_user).values_list('following', flat=True)
    
    # Filter posts where the poster is in the following list
    follow_post = Post.objects.filter(poster__in=following_users).order_by('-last_updated')
    
    # Paginate the posts
    paginator = Paginator(follow_post, 10)
    page_number = request.GET.get('page')
    post_of_page = paginator.get_page(page_number)
    
    # Render the following posts page
    return render(request, "network/following.html", {
        "post_of_page": post_of_page,
    })

from django.http import JsonResponse

def edit(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=post_id, poster=request.user)
            data = json.loads(request.body)
            post.post_content = data.get("content", "")
            post.save()

            # Return the updated content
            return JsonResponse({"messege":"Change Successful","data": post.post_content}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def add_like(request, post_id):
    # This should add a like
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    # Check if a like already exists, if not, add the like
    like, created = Liked.objects.get_or_create(user=user, post=post)
    if created:
        return JsonResponse({"message": "Liked"}, status=200)
    else:
        return JsonResponse({"message": "Already liked"}, status=200)


def remove_like(request, post_id):
    # This should remove the like
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    # Find and delete the like
    like = Liked.objects.filter(user=user, post=post)
    if like.exists():
        like.delete()
        return JsonResponse({"message": "Unliked"}, status=200)
    else:
        return JsonResponse({"message": "Not liked yet"}, status=200)


