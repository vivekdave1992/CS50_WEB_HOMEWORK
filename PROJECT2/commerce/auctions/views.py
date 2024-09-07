from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from .forms import ListingForm
from .models import User,Listing,Category,Comment,Bid


def index(request):
    listings  = Listing.objects.filter(status=True)
    return render(request, 'auctions/index.html', {
        'listings': listings,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user  # Set the seller to the logged-in user
            listing.save()
            return HttpResponseRedirect(reverse("index"))  # Replace with your redirect target
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})



def listing_detail(request, id):
    listing = get_object_or_404(Listing, pk=id)
    is_in_watch_list = False

    if request.user.is_authenticated:
        is_in_watch_list = listing in request.user.watch_list.all()
    all_comments = Comment.objects.filter(listing=listing)
    context = {
        'listing': listing,
        'is_in_watch_list': is_in_watch_list,
        'all_comments':all_comments,
    }
    
    return render(request, 'auctions/listing_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {'categories': categories})


def listings_by_category(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    listing_list = Listing.objects.filter(category=category, status=True)
    return render(request, 'auctions/listings_by_category.html', {'listing_by_category': listing_list,'category':category,})


@login_required
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = get_object_or_404(Listing, id=listing_id)
        user.watch_list.add(listing)
        messages.success(request, f'{listing.title} has been added to your watchlist!')
        return redirect('watchlist')  # Redirect back to the watchlist page
    return redirect('index')  # Redirect to index if method is not POST

@login_required
def remove_from_watchlist(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = get_object_or_404(Listing, id=listing_id)
        user.watch_list.remove(listing)
        messages.success(request, f'{listing.title} has been removed from your watchlist!')
        return redirect('watchlist')  # Redirect back to the watchlist page
    return redirect('index')  # Redirect to index if method is not POST

@login_required
def watchlist(request):
    watchlist = request.user.watch_list.all()  # Ensure it retrieves the listings in the watchlist
    context = {
        'listing_by_category': watchlist,
        'user_name': request.user.username,  # Pass the user's name
    }
    return render(request, 'auctions/watchlist.html', context)



# @login_required
# def remove_multiple_from_watchlist(request):
#     if request.method == 'POST':
#         user = request.user
#         listing_ids = request.POST.getlist('listing_ids')
#         listings = Listing.objects.filter(id__in=listing_ids)
#         user.watch_list.remove(*listings)
#         messages.success(request, 'Selected items have been removed from your watchlist.')
#     return redirect('watchlist')


@login_required
def add_comment (request,listing_id):
    current_user = request.user
    current_listing = get_object_or_404(Listing, id=listing_id)
    message = request.POST.get("New_comment")
    new_commnet = Comment(
        author = current_user,
        listing = current_listing,
        message = message
    )
    new_commnet.save()
    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id, )))


@login_required
def add_bid(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, id=listing_id)
        bid_amount = float(request.POST.get('bid_amount', 0))
        bid_amount = round(bid_amount, 2)
        # Check if the new bid is higher than the current highest bid
        if bid_amount <= listing.highest_bid:
            messages.error(request, 'Bid amount must be higher than the current highest bid.')
            return redirect('listing_detail', id=listing_id)
        # Create the new bid
        new_bid = Bid(
            buyer_user=request.user,
            bid_listing=listing,
            buyer_bid=bid_amount
        )
        new_bid.save()
        # Update the highest bid and bid count
        listing.highest_bid = bid_amount
        listing.bid_count = Bid.objects.filter(bid_listing=listing).count()
        listing.save()
        return redirect('listing_detail', id=listing_id)
    else:
        return redirect('listing_detail', id=listing_id)

