from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime

from .models import User

# Create your views here.
def index(request):

    # Authenticated users view their inbox
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Redirect to welcome if not initiated
    user = request.user
    if not user.weight:
        return HttpResponseRedirect(reverse("welcome"))

    # Everyone else is prompted to sign in
    else:

        goal = user.goal
        weight = user.weight
        initial = user.initial
        start_date = user.start_date
        end_date = user.end_date
        preference = user.metric

        total_days = end_date - start_date
        total_days = total_days.days
        days_left = end_date - datetime.date.today()
        days_left = days_left.days
        days_gone = total_days - days_left

        start_date = start_date.strftime("%d/%m/%Y")
        end_date = end_date.strftime("%d/%m/%Y")

        if days_left >= 0:
            percentage_time = int(days_gone / total_days * 100)
        else:
            percentage_time = 100

        if goal > initial:
            progress = weight - initial
            total = goal - initial
        elif initial > goal:
            progress = initial - weight
            total = initial - goal
        else:
            progress = 1
            total = 1

        percentage = int(progress / total * 100)
        distance = 550 - 550 * percentage / 100 + 5
        distance_time = 550 - 550 * percentage_time / 100 + 5

        try:
            duration = 2000 / percentage
        except ZeroDivisionError:
            duration = 0

        try:
            duration_time = 2000 / percentage_time
        except ZeroDivisionError:
            duration_time = 0
        
        return render(request, "program/index.html", {
            "percentage" : percentage,
            "percentage_time" : percentage_time,
            "distance" : distance,
            "distance_time" : distance_time,
            "duration" : duration,
            "duration_time" : duration_time,
            "initial" : initial,
            "goal" : goal,
            "current" : weight,
            "start_date" : start_date,
            "end_date" : end_date,
            "days" : days_left,
            "preference" : preference
        })


@csrf_exempt
def update(request):

    data = json.loads(request.body)

    new_weight = data.get("new_weight")
    new_goal = data.get("new_goal")
    user = request.user

    user.weight = new_weight
    user.goal = new_goal
    user.save()

    return HttpResponse(status=204)


def welcome(request):

    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        user = request.user
        if user.weight:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "program/welcome.html")

    else: 
        user = request.user
        goal = request.POST["goal"]
        initial = request.POST["initial"]
        end_date = request.POST["end_date"]
        preference = request.POST["preference"]

        if preference == 'imperial':
            user.metric = False
        else:
            user.metric = True

        user.end_date = end_date
        user.goal = goal
        user.initial = initial
        user.weight = initial

        user.save()

        return HttpResponseRedirect(reverse('index'))


def profile(request):

    if request.method == "GET":

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        user = request.user
        if not user.weight:
            return HttpResponseRedirect(reverse("welcome"))

        username = user.username
        goal = user.goal
        start_date = user.start_date
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = user.end_date
        end_date = end_date.strftime("%Y-%m-%d")
        current = user.weight
        initial = user.initial
        preference = user.metric

        return render(request, "program/profile.html", {
            "username": username,
            "goal" : goal,
            "start_date": start_date,
            "end_date": end_date,
            "current" : current,
            "initial" : initial,
            "preference" : preference
        })

    else:

        user = request.user

        goal = request.POST["goal"]
        initial = request.POST["initial"]
        current = request.POST["current"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        preference = request.POST["preference"]

        if preference == 'imperial':
            user.metric = False
        else:
            user.metric = True

        user.end_date = end_date
        user.start_date = start_date
        user.goal = goal
        user.initial = initial
        user.weight = current

        user.save()

        return HttpResponseRedirect(reverse('profile'))




# User authentication
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
            return render(request, "program/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "program/login.html")


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
            return render(request, "program/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "program/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("welcome"))
    else:
        return render(request, "program/register.html")
