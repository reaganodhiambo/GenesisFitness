from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import *
from django.contrib import messages

# Create your views here.
def bookClasses(request):
    user = request.user
    if user.user_type == "member":
        classes = Class.objects.all
        context = {"classes": classes, "user": user}
        return render(request, "templates/Classes/bookClasses.html", context=context)
    else:
        return render(request, "templates/404.html")