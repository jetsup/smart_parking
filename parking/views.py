from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db.utils import IntegrityError
from django.contrib import messages
import bcrypt

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
    return render(request, "advanced-booking.html", {"vehicle_types": vehicle_types})


def about(request: HttpRequest):
    return render(request, "about.html")


def my_admin(request: HttpRequest):
    return render(request, "my-admin.html")


def signup(request: HttpRequest):
    if request.method == "POST":
        print("DATA: ", request.POST)
        user_data = request.POST.dict()
        first_name = user_data.get("first-name")
        last_name = user_data.get("last-name")
        id_number = user_data.get("id-number")
        email = user_data.get("email")
        phone = user_data.get("phone")
        rfid = user_data.get("rfid")
        password = str(user_data.get("password"))
        password_confirmation = str(user_data.get("password_confirmation"))
        username = email
        remember = user_data.get("remember")

        print(
            "USER:",
            first_name,
            last_name,
            id_number,
            email,
            phone,
            rfid,
            password,
            username,
            remember,
            ":>>>>",
        )
        # Check if passwords match
        if password != password_confirmation:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect('signup')
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                username=username,
                id_passport=id_number,
                password=password,
                is_superuser=False,
                user_type=2,
                rfid=rfid,
            )
            user.save()
            authentic_user = authenticate(request, username=username, password=password)
            if authentic_user:
                login(request, user)
                print(" ------------------- USER: ", user)
                return redirect("home")
            return redirect("signin")
        except IntegrityError as e:
            print("Duplicate Error: ", e)
            return redirect("home")
    elif request.method == "GET":
        return render(request, "register.html")


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


def signout(request: HttpRequest):
    logout(request)
    return redirect("home")
