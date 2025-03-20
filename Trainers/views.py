from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import CustomUser
from Base.models import *
from Accounts.models import *   
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def trainerDashboard(request):
    user = request.user
    if user.user_type == "trainer":
        trainers = Trainer.objects.all()
        profile = get_object_or_404(CustomUser, id_number=user.id_number)
        context = {"trainers": trainers, "user": user, "profile": profile}
        return render(request, "templates/Trainers/trainers.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def viewProfile(request, id_number):
    profile = get_object_or_404(CustomUser, id_number=id_number)
    context = {"profile": profile}
    return render(request, "templates/viewProfile.html", context)


# @login_required
# def editProfile(request, id_number):
#     profile = get_object_or_404(CustomUser, id_number=id_number)
#     if request.method == "POST":
#         form = EditProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request,
#                 "Profile Updated successfully",
#                 extra_tags="success",
#             )
#             return redirect("trainers")
#     else:
#         form = EditProfileForm(instance=profile)
#     context = {"profile": profile, "form": form}
#     return render(request, "templates/editProfile.html", context)


@login_required
def viewClasses(request, id_number):
    profile = get_object_or_404(CustomUser, id_number=id_number)
    classes = Class.objects.filter(trainer_name=profile)
    context = {"profile": profile, "classes": classes}
    return render(request, "templates/Classes/viewClasses.html", context)


@login_required
def viewMembers(request):
    trainer = request.user
    if trainer.user_type == "trainer":
        bookings = Booking.objects.filter(trainer_name=trainer)
        context = {"bookings": bookings, "trainer": trainer}
        return render(request, "templates/trainer_members.html", context)
    else:
        return render(request, "templates/404.html")
