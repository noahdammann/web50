from email import message
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Watchlist, Bid


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
    })


def add(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/add.html", {
            "categories" : categories
        })

    else:
        # Get form data
        title = request.POST["title"]
        description = request.POST["description"]
        price = float(request.POST["price"])
        img_url = request.POST["img_url"]
        category = request.POST["category"]

        # Get user information
        user = request.user

        # Get category
        category_in_db = Category.objects.get(categoryName=category)

        # Create new Listing
        listing = Listing(title=title, description=description, price=price, img_url=img_url, category=category_in_db, owner=user)

        # Save listing in Bid model
        new_bid = Bid(listing=listing, owner=user)

        # Save listing and bid
        listing.save()
        new_bid.save()

        # Render index
        return HttpResponseRedirect(reverse("index"))

def listing_page(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        comments = Comment.objects.filter(listing=listing)
        user = request.user
        try:
            watchlist = Watchlist.objects.get(listing=listing, user=user)
        except:
            watchlist = None
        bid = Bid.objects.get(listing=listing)
        if bid.winner == True and bid.owner == user:
            winner = bid.owner
        else:
            winner = None
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "comments" : comments,
            "watchlist" : watchlist,
            "winner" : winner
        })

    else: 
        message = request.POST["comment"]
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment(message=message, creator=user, listing=listing)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.status = False
    listing.save()
    bid = Bid.objects.get(listing=listing)
    bid.winner = True
    bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.get(user=user)
        watchlist.listing.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    else:
        user = request.user
        watchlist = Watchlist.objects.get(user=user)
        listings = watchlist.listing.all()
        return render(request, "auctions/watchlist.html", {
            "listings" : listings
        })


def remove_from_watchlist(request):
    listing_id = request.POST["remove_from_watchlist"]
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    favorites = Watchlist.objects.get(user=user)
    favorites.listing.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def categories(request):
    category_fields = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : category_fields
    })


def category(request, categoryName):
    category_field = Category.objects.get(categoryName=categoryName)
    listings = Listing.objects.filter(category=category_field)
    return render(request, "auctions/category.html", {
        "category" : category_field,
        "listings" : listings
    })


def bid(request):
    if request.method == "POST":
        new_price = float(request.POST["value"])
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        current_price = listing.price
        if new_price <= current_price:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        listing.price = new_price
        listing.save()
        user = request.user
        old_bid = Bid.objects.get(listing=listing)
        old_bid.owner = user
        old_bid.save()
        return HttpResponseRedirect(reverse("index"))


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

            # Create watchlist
            watchlist = Watchlist(user=user)
            watchlist.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
