from __future__ import unicode_literals
from django.db import models
from django.contrib import messages             #check this one if we need it in this page
import re                                       #check this one if we need it in this page
import md5
import os, binascii
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        if len(postData['fullname']) < 2:
            errors.append("Full Name should be more than 2 characters")
        elif not NAME_REGEX.match(postData['fullname']):
            errors.append("Full Name: Please use letters only.")
        if len(postData['username']) < 2:
            errors.append("Username should be more than 2 characters")
        elif not NAME_REGEX.match(postData['username']):
            errors.append("Username: Please use letters only.")
        if len(postData['password']) < 8:
            errors.append("Password should be no less than 8 characters")
        elif postData['password'] != postData['password_confirm']:
            errors.append("Password is not matched. Please again")
            
#if there's no error then password 
        if len(errors) == 0 :
             # if username is found in db
            salt = binascii.b2a_hex(os.urandom(15)) 
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
             # add to database
            User.objects.create(fullname=postData['fullname'], username=postData['username'], salt=salt, password=hashed_pw)
        return errors

    def login(self, postData):
        errors = []
        # if username is found in db
        if User.objects.filter(username=postData['username']):
            salt = User.objects.get(username=postData['username']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            # compare hashed passwords
            if User.objects.get(username=postData['username']).password != hashed_pw:
                errors.append('Incorrect password')
        # else if username is not found in db
        else:
            errors.append('username has not been registered')
        return errors

class User(models.Model):
    fullname = models.CharField(max_length=255, default= "")
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "user object: ---,{} ----{}".format(self.fullname, self.username)

class Travel(models.Model):
    destination = models.CharField(max_length=255, default= "")
    user = models.ForeignKey(User, related_name="names")
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    join = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "travel object: ---,{} ----{} ----{} ----{} ----{}".format(self.destination, self.start, self.end, self.plan, self.join)