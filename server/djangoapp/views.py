from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealers_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import uuid

import requests as req

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context["warning"] = "Cannot login: Either Username or Password are wrong."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # <HINT> Get user information from request.POST
        # <HINT> username, first_name, last_name, password
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            # User.objects.get(username=username)
            user_exist = True
        else:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            context["warning"] = "User exists. Please login."
            return render(request, 'djangoapp/registration.html', context)
    else:
        return HttpResponse("Wrong Method")

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    # context = req.get(https://sdyeung-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get)
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = "https://dealerships-list.1d8af0j7quu7.us-south.codeengine.appdomain.cloud/dealerships/get"
        # Get dealers from the URL
        dealerships_list = get_dealers_from_cf(url)
        
        #dealerships_list = get_dealers_by_id(url)
        # Concat all dealer's short name
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', {"dealerships_list": dealerships_list})


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = 'https://review.1d8af0j7quu7.us-south.codeengine.appdomain.cloud/api/get_reviews'
        reviews_list = get_dealer_reviews_from_cf(url,dealer_id)
        dealer_url = "https://dealerships-list.1d8af0j7quu7.us-south.codeengine.appdomain.cloud/dealerships/get"
        dealership = get_dealers_by_id(dealer_url,dealerId=dealer_id)
        return render(request, 'djangoapp/dealer_details.html', {"reviews_list": reviews_list, "dealer": dealership[0]})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == 'GET':
        cars = CarModel.objects.filter(dealerid=dealer_id)
        dealer_url = "https://dealerships-list.1d8af0j7quu7.us-south.codeengine.appdomain.cloud/dealerships/get"
        dealership = get_dealers_by_id(dealer_url,dealerId=dealer_id)
        
        return render(request, 'djangoapp/add_review.html', {"dealer": dealership[0],"cars": cars})
    elif request.method == 'POST':
        #car = CarModel.objects.get(id=request.POST['car'])
        car = request.POST['car'].split("-")
        review=dict()
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["id"] = car[0]
        review["name"] = f"{request.user.first_name} {request.user.last_name}"
        review["purchase"] = True
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = car[1]
        review["car_model"] = car[2]
        review["car_year"] = car[3]

        json_payload = review

        url = 'https://review.1d8af0j7quu7.us-south.codeengine.appdomain.cloud/api/post_review'

        json_result = post_request(url, json_payload, dealerId=dealer_id)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    else:
        return HttpResponse("Wrong Method")





