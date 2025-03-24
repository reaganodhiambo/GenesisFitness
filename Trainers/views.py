from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import CustomUser
from Base.models import *
from Accounts.models import *
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


@login_required
def generate_report(request):
    user = request.user
    if user.user_type == "trainer":
        # Get all bookings for the trainer
        bookings = Booking.objects.filter(trainer_name=user)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="class_members_report.pdf"'
        )

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Draw the title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "Class Members Report")

        # Draw the table headers
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 100, "First Name")
        p.drawString(150, height - 100, "Last Name")
        p.drawString(250, height - 100, "Email")
        p.drawString(350, height - 100, "Phone Number")
        p.drawString(450, height - 100, "Class Booked")

        # Draw the table rows
        p.setFont("Helvetica", 12)
        y = height - 120
        for booking in bookings:
            p.drawString(50, y, booking.client_name.first_name)
            p.drawString(150, y, booking.client_name.last_name)
            p.drawString(250, y, booking.client_name.email)
            p.drawString(350, y, str(booking.client_name.phone_number))
            p.drawString(450, y, booking.class_name.class_name)
            y -= 20

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        return response
    else:
        return render(request, "templates/404.html")
