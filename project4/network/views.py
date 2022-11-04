import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


@csrf_exempt
@login_required
def post(request, post_id):
    edited_post = Post.objects.get(id=post_id)
    data = json.loads(request.body)
    content = data.get("content")
    edited_post.content = content
    edited_post.save()
    return HttpResponse(status=204)


@csrf_exempt
@login_required
def add(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get content for post
    data = json.loads(request.body)
    content = data.get("content")

    # Add the post to the database
    user = request.user
    new_post = Post(creator=user, content=content)
    new_post.save()

    return JsonResponse({"message": "Post was added successfully"}, status=201)



@csrf_exempt
def send_feed(request, feed, page):
    
    # Filter posts to send based on feed
    if feed == "main":
        posts = Post.objects.all()
    elif feed == "following":
        people_followed = request.user.following.all()
        posts = Post.objects.filter(creator__in=people_followed).all()
    else:
        return JsonResponse({"error": "Invalid feed"}, status=400)

    # Return posts in reverse chronological order
    posts = posts.order_by("-time").all()
    p = Paginator(posts, 10)
    page_obj = p.page(page)
    return JsonResponse({
        "posts" : [post.serialize() for post in page_obj],
        "num_pages" : p.num_pages
    }
    , safe=False)

@csrf_exempt
@login_required
def profile(request, username):

    user = request.user
    
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


    if request.method == "GET":
        return JsonResponse(profile_user.serialize())


    # Put requests
    elif request.method == "PUT":
        data = json.loads(request.body)

        # Update following
        if data.get("follow") is not None:
            if profile_user in user.following.all():
                user.following.remove(profile_user)
            else:
                user.following.add(profile_user)
            user.save()       

        # Return HttpResonse
        return HttpResponse(status=204)



    # Profile must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def like_post(request, post_id):

    user = request.user

    post = Post.objects.get(id=post_id)

    # Add or remove like appropriately
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    post.save()

    likes = post.likes.all().count()
    return HttpResponse(status=203)




















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
