from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import CustomUser
from Base.models import *
from Accounts.models import *
from django.contrib.auth.models import User
from .forms import EditProfileForm, MemberFilterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

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
        form = MemberFilterForm(request.GET or None)
        bookings = Booking.objects.filter(trainer_name=trainer)

        if form.is_valid():
            class_name = form.cleaned_data.get("class_name")
            booking_date = form.cleaned_data.get("booking_date")
            day_of_week = form.cleaned_data.get("day_of_week")

            if class_name:
                bookings = bookings.filter(class_name=class_name)
            if booking_date:
                bookings = bookings.filter(booking_date=booking_date)
            if day_of_week:
                bookings = bookings.filter(class_name__day_of_week=day_of_week)

        context = {"bookings": bookings, "trainer": trainer, "form": form}
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
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add heading and contact information
        styles = getSampleStyleSheet()
        title = Paragraph("Class Members Report", styles["Title"])
        contact_info = Paragraph(
            f"Trainer: {user.first_name} {user.last_name}<br/>Email: {user.email}",
            styles["Normal"],
        )
        elements.append(title)
        elements.append(contact_info)

        # Add some space
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))

        # Create the table data
        data = [["First Name", "Last Name", "Email", "Phone Number", "Class Booked"]]
        for booking in bookings:
            data.append(
                [
                    booking.client_name.first_name,
                    booking.client_name.last_name,
                    booking.client_name.email,
                    str(booking.client_name.phone_number),
                    booking.class_name.class_name,
                ]
            )

        # Create the table
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        elements.append(table)

        # Build the PDF
        doc.build(elements)

        return response
    else:
        return render(request, "templates/404.html")
