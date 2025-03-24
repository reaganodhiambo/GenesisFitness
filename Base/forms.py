from django import forms
from .models import Class, Booking, Membership
from django.utils import timezone
from datetime import date


class AddClassesForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"
        exclude = ["trainer_name"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "starting_time": forms.TimeInput(attrs={"type": "time"}),
            "ending_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        starting_time = cleaned_data.get("starting_time")
        ending_time = cleaned_data.get("ending_time")

        if starting_time and ending_time and starting_time >= ending_time:
            raise forms.ValidationError(
                "Starting time must be earlier than ending time."
            )

        return cleaned_data


class BookClassForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["class_name"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Get user from kwargs
        super(BookClassForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["class_name"].queryset = (
                Class.objects.all()
            )  # Or filter as needed
            self.user = user

    def clean(self):
        cleaned_data = super().clean()
        class_instance = cleaned_data.get("class_name")

        if self.user and class_instance:
            if not Booking.is_booking_allowed(self.user, class_instance):
                raise forms.ValidationError(
                    "You need an active membership to book this class."
                )

            existing_booking = Booking.objects.filter(
                client_name=self.user,
                class_name=class_instance,
                booking_date=timezone.now().date(),
            ).exists()

            if existing_booking:
                raise forms.ValidationError("You have already booked this class today.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.client_name = self.user  # Set client name to the passed in user.
        if commit:
            instance.save()
        return instance


class MembershipForm(forms.ModelForm):
    MEMBERSHIP_TYPE_CHOICES = (
        ("weekly", "Weekly - 2000 KES"),
        ("monthly", "Monthly - 7500 KES"),
    )
    membership_type = forms.ChoiceField(choices=MEMBERSHIP_TYPE_CHOICES)

    class Meta:
        model = Membership
        fields = ["membership_type"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # get the user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        membership_type = self.cleaned_data["membership_type"].split(" - ")[
            0
        ]  # Extract the type without price
        start_date = date.today()
        membership = Membership.create_membership(
            self.user, membership_type, start_date
        )
        return membership
