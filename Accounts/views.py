from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.http import HttpResponse
from .models import *


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        profile = get_object_or_404(CustomUser, id_number=request.user.id_number)
        
    else:
        user_type = None
        profile = None
    context = {"user_type": user_type, "profile": profile}
    return render(request, "templates/home.html",context=context)


def registerUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")
        else:
            form = UserRegistrationForm()

    return render(request, "templates/register.html", {"form": form})


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = request.user.user_type
            print(user_type)
            if user_type == "trainer":
                return redirect("trainers")
            else:
                return redirect("members")
        else:
            messages.error(request, "Invalid username or password")

    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "templates/login.html", context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")


def memberDashboard(request):
    user = request.user
    if user.user_type == "member":
        trainers = Trainer.objects.all()
        profile = get_object_or_404(CustomUser, id_number=user.id_number)
        context = {"trainers": trainers, "user": user, "profile": profile}
        return render(request, "templates/members.html", context=context)
    else:
        return render(request, "templates/404.html")


def viewProfile(request, id_number):
    profile = get_object_or_404(CustomUser, id_number=id_number)
    context = {"profile": profile}
    return render(request, "templates/viewProfile.html", context)


def editProfile(request, id_number):
    profile = get_object_or_404(CustomUser, id_number=id_number)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile Updated successfully",
                extra_tags="success",
            )
            if request.user.user_type == "trainer":
                return redirect("members")
            else:
                return redirect("trainers")
    else:
        form = EditProfileForm(instance=profile)
    context = {"profile": profile, "form": form}
    return render(request, "templates/editProfile.html", context)
