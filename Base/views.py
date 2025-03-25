from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import CustomUser
from Base.models import *
from Base.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from datetime import datetime
import os


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
        # Check if the user has an active membership
        active_membership = Membership.objects.filter(
            client_name=user,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).exists()

        if not active_membership:
            messages.error(request, "You need an active membership to book classes.")
            return redirect("membership")

        filter_form = ClassFilterForm(request.GET or None)
        classes = Class.objects.all()

        if filter_form.is_valid():
            class_name = filter_form.cleaned_data.get("class_name")
            trainer_name = filter_form.cleaned_data.get("trainer_name")
            day_of_week = filter_form.cleaned_data.get("day_of_week")

            if class_name:
                classes = classes.filter(class_name__icontains=class_name)
            if trainer_name:
                classes = classes.filter(
                    trainer_name__first_name__icontains=trainer_name
                ) | classes.filter(trainer_name__last_name__icontains=trainer_name)
            if day_of_week:
                classes = classes.filter(day_of_week=day_of_week)

        profile = get_object_or_404(CustomUser, id_number=id_number)

        if request.method == "POST":
            form = BookClassForm(request.POST, user=user)
            if form.is_valid():
                class_instance = form.cleaned_data["class_name"]
                Booking.register_member(user, class_instance)
                messages.success(request, "Class booked successfully")
                return redirect("viewBookedClasses")
            else:
                messages.error(request, form.errors)

        else:
            form = BookClassForm(user=user)

        context = {
            "classes": classes,
            "user": user,
            "profile": profile,
            "form": form,
            "filter_form": filter_form,
        }
        return render(request, "templates/Classes/bookClasses.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def membership(request):
    user = request.user
    if user.user_type == "member":
        # Check if the user has an active membership
        active_membership = Membership.objects.filter(
            client_name=user,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).exists()

        if active_membership:
            messages.info(request, "You already have an active membership.")
            return redirect("viewMembership")

        if request.method == "POST":
            form = MembershipForm(request.POST, user=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Membership created successfully")
                return redirect("bookClasses", id_number=user.id_number)
            else:
                messages.error(request, form.errors)
        else:
            form = MembershipForm(user=user)

        context = {"form": form}
        return render(request, "templates/membership.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def viewMembership(request):
    user = request.user
    if user.user_type == "member":
        membership = (
            Membership.objects.filter(client_name=user).order_by("-end_date").first()
        )
        context = {"membership": membership}
        return render(request, "templates/viewMembership.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def viewBookedClasses(request):
    user = request.user
    if user.user_type == "member":
        bookings = Booking.objects.filter(client_name=user)
        context = {"bookings": bookings}
        return render(request, "templates/viewBookedClasses.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def cancelBooking(request, booking_id):
    user = request.user
    if user.user_type == "member":
        booking = get_object_or_404(Booking, id=booking_id, client_name=user)
        if request.method == "POST":
            booking.delete()
            messages.success(request, "Booking canceled successfully")
            return redirect("viewBookedClasses")
        context = {"booking": booking}
        return render(request, "templates/cancelBooking.html", context=context)
    else:
        return render(request, "templates/404.html")


@login_required
def generate_membership_report(request):
    user = request.user
    if user.user_type == "member":
        # Get the user's membership details
        membership = (
            Membership.objects.filter(client_name=user).order_by("-end_date").first()
        )

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="membership_report.pdf"'

        # Create the PDF object, using the response object as its "file."
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add heading and user details
        styles = getSampleStyleSheet()
        title = Paragraph("Membership Report", styles["Title"])
        user_details = Paragraph(
            f"User: {user.first_name} {user.last_name}<br/>Email: {user.email}<br/>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
        elements.append(title)
        elements.append(user_details)

        # Add some space
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))

        # Create the table data
        data = [
            ["Membership Type", "Start Date", "End Date", "Price", "Status"],
            [
                membership.membership_type,
                membership.start_date,
                membership.end_date,
                f"{membership.price} KES",
                membership.status,
            ],
        ]

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

        # Add footer
        footer = Paragraph("Generated by Genesis Fitness", styles["Normal"])
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))
        elements.append(footer)

        # Build the PDF
        doc.build(elements)

        return response
    else:
        return render(request, "templates/404.html")


@login_required
def generate_booked_classes_report(request):
    user = request.user
    if user.user_type == "member":
        # Get the user's booked classes
        bookings = Booking.objects.filter(client_name=user)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="booked_classes_report.pdf"'
        )

        # Create the PDF object, using the response object as its "file."
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add logo
        logo_path = os.path.join("static", "images", "logo.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=100, height=50)
            elements.append(logo)

        # Add heading and user details
        styles = getSampleStyleSheet()
        title = Paragraph("Booked Classes Report", styles["Title"])
        user_details = Paragraph(
            f"User: {user.first_name} {user.last_name}<br/>Email: {user.email}<br/>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
        elements.append(title)
        elements.append(user_details)

        # Add some space
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))

        # Create the table data
        data = [
            ["Class Name", "Instructor", "Day", "Start Time", "End Time"],
        ]
        for booking in bookings:
            data.append(
                [
                    booking.class_name.class_name,
                    f"{booking.trainer_name.first_name} {booking.trainer_name.last_name}",
                    booking.class_name.day_of_week,
                    booking.class_name.starting_time,
                    booking.class_name.ending_time,
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

        # Add footer
        footer = Paragraph("Generated by Genesis Fitness", styles["Normal"])
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))
        elements.append(footer)

        # Build the PDF
        doc.build(elements)

        return response
    else:
        return render(request, "templates/404.html")
