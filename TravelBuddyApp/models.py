from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt


class LoginManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['form_name']) < 3:
            errors['form_name'] = "User's name should be at least 3 characters"
        if len(postData['form_username']) < 3:
            errors['form_username'] = "User's username should be at least 3 characters"
        if postData['form_password'] != postData['form_confirm_pw']:
            errors['form_password'] = "Passwords don't match"
        if len(postData['form_password']) < 8:
            errors["form_password"] = "Password should be at least 8 characters"
        usersWithUsername = User.objects.filter(username=postData['form_username'])
        if len(usersWithUsername) > 0:
            errors['form_username'] = "Username already exists!"
        print(errors)
        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['form_username']) < 1:
            errors['username'] = "Username required to login"
        userMatch = User.objects.filter (username = postData['form_username'])
        if len(userMatch) == 0:
            errors['null'] = "Username could not be found, register new username"
        else:
            user = userMatch[0]
            if bcrypt.checkpw(postData['form_password'].encode(), user.password.encode()):
                print("password matches")
            else:
                errors['pwmatch'] = "Incorrect Password"
        return errors


    def trip_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['form_destination']) < 2:
            errors["destination"] = "Destination should be at least 1 character"
        if len(postData['form_description']) < 3:
            errors["description"] = "Description should be at least 1 character"
            print(postData['form_travelStartDate'])
        start = datetime.strptime(postData['form_travelStartDate'], "%Y-%m-%d")
        end = datetime.strptime(postData['form_travelEndDate'], "%Y-%m-%d")
        present = datetime.now()
        if start.date() < present.date():
            errors["travelStartDate"] = "Trip is scheduled for the past."
        if start.date() > end.date():
            print("START LESS END")
            errors["travelStartDate"] = "Trip End Date is before Start Date"
        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    confirm_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    travelStartDate = models.DateField()
    travelEndDate = models.DateField()
    added_by = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)
    travelers = models.ManyToManyField(User, related_name="travelers_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

