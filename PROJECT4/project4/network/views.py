from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User,Post,PostComment,Follow


def index(request):
    all_post= Post.objects.all().order_by('last_updated').reverse()
    paginator = Paginator(all_post,10)
    page_number = request.GET.get('page')
    post_of_page = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "all_post":all_post,
        "post_of_page":post_of_page,
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
    user = User.objects.get(pk=user_id)
    all_post= Post.objects.filter(poster=user).order_by('last_updated').reverse()
    paginator = Paginator(all_post,10)
    page_number = request.GET.get('page')
    post_of_page = paginator.get_page(page_number)
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    return render(request, "network/profile.html",{
        "all_post":all_post,
        "post_of_page":post_of_page,
        "username":user,
        "followers_count":followers_count,
        "following_count":following_count
    })
