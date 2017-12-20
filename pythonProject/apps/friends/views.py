# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, HttpResponse, redirect
from .models import User, Friend
from django.contrib import messages



# Create your views here.


def home(request):
    return render(request, 'friends/home.html')

def register(request):
    response = User.objects.register(
        request.POST["name"],
        request.POST["alias"],
        request.POST["email"],
        request.POST["password"],
        request.POST["confirm"],
        request.POST["dob"]

    )
    print response

    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/profile")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def login(request):
    response = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )

    if response["valid"]: 
        request.session["user_id"] = response["user"].id 
        return redirect("/profile")
    else: 
        for error_message in response["errors"]: 
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def profile(request):
    # User.objects.all().delete()
    # Friend.objects.all().delete()

    admin = User.objects.get(id=request.session['user_id'])
    others = []
    friend = Friend.objects.filter(user=admin)
    not_friends = User.objects.all().exclude(id=admin.id)

    for x in friend:
        not_friends = not_friends.exclude(id=x.friend.id)

    context = {
        "user": admin,
        "friends": friend,
        "not_friends": not_friends

        }

    return render(request, 'friends/profile.html', context)

def add(request, id):
    Friend.objects.addFriend(request.session['user_id'], id) 
    return redirect("/profile")


def remove(request, id):
    Friend.objects.deleteFriend(request.session["user_id"], id)
    return redirect("/profile")


def friendInfo(request, id):
    user = User.objects.get(id=id)
    print "hello"
    return render(request, 'friends/friendInfo.html', {"user": user} )
    
    



    