from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "id_number", "phone_number", "user_type"]


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
