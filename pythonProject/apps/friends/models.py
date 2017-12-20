# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


class UserManager(models.Manager):
    def register(self, name, alias, email, password, confirm, dob):
        print 'inside regester methods'
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(name) < 1:
            response["errors"].append("First and Last name required")
        elif len(name) < 3:
            response["errors"].append("name must be 3 characters or longer")

        if len(alias) < 1:
            response["errors"].append("Alias is required")
        elif len(alias) < 3:
            response["errors"].append("Alias must be 3 characters or longer")

        if len(email) < 1:
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email):
            response["errors"].append("Invalid Email")
        else:
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) > 0:
                response["errors"].append("Email is already in use")

        if len(dob) < 1:
            response["errors"].append("Date of Birth is required")
        else:
            date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.now()
            if date > today:
                response["errors"].append("Date of Birth must be in the past")

        if len(password) < 1:
            response["errors"].append("Password is required")
        elif len(password) < 8:
            response["errors"].append("Password must be 8 characters or longer")

        if len(confirm) < 1:
            response["errors"].append("Confirm Password is required")
        elif confirm != password:
            response["errors"].append("Confirm Password must match Password")

        if len(response["errors"]) > 0:
            response["valid"] = False
            print 'there were errors'
        else:
            print 'user was created'
            response["user"] = User.objects.create(

                name=name,
                alias=alias,
                email=email.lower(),
                dob=date,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            )
        return response 

    def login(self, email, password): 
        response = {
            "valid": True, 
            "errors": [],
            "user": None
        }

        if len(email) < 1: 
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email): 
            response["errors"].append("Invalid Email")
        else: 
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) == 0: 
                response["errors"].append("Email is already in use.")
        
        if len(password) < 1: 
            response["errors"].append("Password is required")
        elif len(password) < 8: 
            response["errors"].append("Password must be 8 character or longer")

        if len(response["errors"]) == 0:
            hashed_pw = email_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response["user"] = email_list[0]
            else: 
                response["errors"].append("Password is incorrect")
        if len(response["errors"]) > 0:
            response["valid"] = False 

        return response

class FriendManager(models.Manager):
    def addFriend(self, user_id, friend_id):
        send = User.objects.get(id=user_id)
        receive = User.objects.get(id=friend_id)
        Friend.objects.create(user=send, friend=receive)
        Friend.objects.create(user=receive, friend=send)
        
    def deleteFriend(self, user_id, friend_id):
        send = User.objects.get(id=user_id)
        print send
        receive = User.objects.get(id=friend_id)
        print receive
        Friend.objects.get(user=send, friend=receive).delete()
        Friend.objects.get(user=receive, friend=send).delete()

        

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    # def __repr__(self):
    #     return "User {} {}".format(self.id, self.alias)

class Friend(models.Model):
    user = models.ForeignKey(User, related_name="send")
    friend = models.ForeignKey(User, related_name="receive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FriendManager()

    # def __repr__(self):
    #     return "Friend {} {}".format(self.user_id, self.friend_id)
    


    
        
    
    

