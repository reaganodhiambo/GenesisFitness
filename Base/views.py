from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import *
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def addClasses(request):
    user = request.user
    if user.user_type == "trainer":
        if request.method == "POST":
            form = AddClassesForm(request.POST)
            if form.is_valid():
                class_instance = form.save(commit=False)
                class_instance.trainer_name = user
                class_instance.save()
                messages.success(request, "Class added successfully")
                return redirect("viewClasses", id_number=user.id_number)
        else:
            form = AddClassesForm()
        context = {"form": form}
        return render(request, "templates/Classes/addClasses.html", context=context)


def about(request):
    return render(request, "templates/about.html")


def contact(request):
    return render(request, "templates/contact.html")


def editClasses(request, id):
    user = request.user
    if user.user_type == "trainer":
        class_instance = get_object_or_404(Class, id=id)
        if request.method == "POST":
            form = AddClassesForm(request.POST, instance=class_instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Class updated successfully")
                return redirect("viewClasses", id_number=user.id_number)
        else:
            form = AddClassesForm(instance=class_instance)
        context = {"form": form}
        return render(request, "templates/Classes/editClass.html", context=context)


def deleteClasses(request, id):
    user = request.user
    if user.user_type == "trainer":
        class_instance = get_object_or_404(Class, id=id)
        if request.method == "POST":
            class_instance.delete()
            messages.success(request, "Class deleted successfully")
            return redirect("viewClasses", id_number=user.id_number)
        context = {"class_instance": class_instance}
        return render(request, "templates/Classes/deleteClass.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def bookClasses(request, id_number):
    user = request.user
    if user.user_type == "member":
        classes = Class.objects.all()
        profile = get_object_or_404(CustomUser, id_number=id_number)

        if request.method == "POST":
            class_id = request.POST.get("class_id")
            class_instance = get_object_or_404(Class, id=class_id)
            Booking.register_member(user, class_instance)
            messages.success(request, "Class booked successfully")
            return redirect("bookClasses", id_number=id_number)

        context = {"classes": classes, "user": user, "profile": profile}
        return render(request, "templates/Classes/bookClasses.html", context=context)
    else:
        return render(request, "templates/404.html")
