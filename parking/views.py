from django.shortcuts import render, redirect
from django.http import HttpRequest

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *


# Create your views here.
def home(request: HttpRequest):
    return render(request, "index.html")


def access(request: HttpRequest):
    return render(request, "access.html")


def parking(request: HttpRequest):
    return render(request, "parking.html")


def advanced_booking(request: HttpRequest):
    vehicle_types = VehicleTypes.objects.all()
    print(vehicle_types)
    return render(request, "advanced-booking.html", {"vehicle_types":vehicle_types})


def about(request: HttpRequest):
    return render(request, "about.html")


def my_admin(request: HttpRequest):
    return render(request, "my-admin.html")


def signin(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
        req = request.POST
        username = req.get("username")
        password = req.get("psw")
        remember = req.get("remember")

        user = authenticate(request, email=username, password=password)
        print("USER:", user)
        if user is not None:
            login(request, user)
            # if remember = on, maintain user session for long
            return redirect("home")
        else:
            return redirect("signin")
    elif request.method == "GET":
        return render(request, "login.html")


def signup(request: HttpRequest):
    logout(request)
    return redirect("home")
