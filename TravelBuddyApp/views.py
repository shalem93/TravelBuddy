from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q


def load(request):
    return redirect("/main")


def index(request):
    return render(request, "index.html")

def registerUser(request):
    errors = User.objects.registrationValidator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        password = request.POST['form_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
        print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
        User.objects.create(name=request.POST['form_name'], username=request.POST['form_username'], password=pw_hash) 
        return redirect('/')

def loginUser(request):
    errors = User.objects.loginValidator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.filter(username=request.POST['form_username']) # why are we using filter here instead of get?
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['form_password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['userid'] = logged_user.id
            # never render on a post, always redirect!
            return redirect('/travels')
        
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    
    return redirect("/")

def travels(request):
    if 'userid' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['userid'])
        allTrips = Trip.objects.all()
        context = {
            'user' : user,
            'alltrips': allTrips,
            'mytrips': Trip.objects.filter(added_by = user) | Trip.objects.filter(travelers = user),
            'othertrips': Trip.objects.exclude(Q(added_by = user) | Q(travelers = user)),
        }
        return render(request, "travels.html", context)

def createTrip(request):
    print(request.POST)
    errors = Trip.objects.trip_validator(request.POST)
    user = User.objects.get(id=request.session['userid'])
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/travels/add')
    else:
        newTrip = Trip.objects.create(destination = request.POST['form_destination'], description = request.POST['form_description'], travelStartDate = request.POST['form_travelStartDate'], travelEndDate = request.POST['form_travelEndDate'], added_by = user)
    return redirect("/travels")

def newTrip(request):
    return render(request, "addTrip.html")

def joinTrip(request, tripID):
    user = User.objects.get(id= request.session['userid'])
    joinTrip = Trip.objects.get(id = tripID)
    joinTrip.travelers.add(user)
    return redirect("/travels")

def viewTrip(request, tripID):
    viewTrip = Trip.objects.get(id = tripID)
    context = {
        'trip': viewTrip,
    }
    return render(request, "destination.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")