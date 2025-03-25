from .models import *
from Accounts.models import *
from django import forms
from Base.models import Class


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone_number": "Phone Number",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }


class MemberFilterForm(forms.Form):
    class_name = forms.ModelChoiceField(
        queryset=Class.objects.all(), required=False, label="Class Name"
    )
    booking_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Booking Date",
    )
    day_of_week = forms.ChoiceField(
        choices=[("", "---------")] + list(Class.DAYS_OF_WEEK),
        required=False,
        label="Day of the Week",
    )
