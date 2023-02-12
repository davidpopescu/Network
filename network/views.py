import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    return render(request, "network/index.html", {
        "posts": paginator.get_page(page_number)
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

def newPost(request):
    if (request.method == 'POST' and request.POST["content"] != ""):
        post = Post(user=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else :
        return HttpResponseRedirect(reverse("index"))

def allPosts(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    return render(request, "network/index.html", {
        "posts": paginator.get_page(page_number)
    })

@login_required
def following(request):
    profile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(user__in=profile.following.all()).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    if profile.following.count() > 0:
        return render(request, "network/following.html", {
            "posts": paginator.get_page(page_number)
        })
    else:
        return HttpResponseRedirect(reverse("index"))

def profile(request, id):
    user = User.objects.get(id=id)
    if not Profile.objects.filter(user=user).exists():
        profile = Profile(user=user)
        profile.save()
    profile = Profile.objects.get(user = user)
    posts = Post.objects.all().filter(user=user).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    followers = user.following.count()
    following = user.followers.count()
    page_number = request.GET.get('page')
    return render(request, "network/profile.html", {
        "user": user,
        "currentUser" : request.user,
        "posts": paginator.get_page(page_number),
        "followers": followers,
        "following": following,
        "profile": profile
    })

def follow(request, id):
    user = User.objects.get(id=id)
    profile2 = Profile.objects.get(user = request.user)
    profile2.following.add(user)
    profile2.save()
    profile = Profile.objects.get(user = user)
    profile.followers.add(request.user)
    return HttpResponseRedirect(reverse("profile", args=(id,)))

def unfollow(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    profile.followers.remove(request.user)
    profile.save()
    profile2 = Profile.objects.get(user = request.user)
    profile2.following.remove(User.objects.get(id=id))
    profile2.save()
    return HttpResponseRedirect(reverse("profile", args=(id,)))

@csrf_exempt
def edit(request, id):
    post = Post.objects.get(id=id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.content = data.get("post")
            post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        if data.get("liked") is not None:
            if data.get("liked") is True: 
                post.likesNumber = post.likesNumber + 1
                post.save()
            else:
                post.likesNumber = post.likesNumber - 1
                post.save()
        return HttpResponse(status=204)
