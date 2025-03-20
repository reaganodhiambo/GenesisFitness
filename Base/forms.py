from django import forms
from django.core.exceptions import ValidationError
from .models import Class


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
            raise ValidationError("Starting time must be earlier than ending time.")

        return cleaned_data


class BookClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            "class_name",
            "trainer_name",
            "start_date",
            "starting_time",
            "ending_time",
        ]
        widgets = {
            "members": forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        starting_time = cleaned_data.get("starting_time")
        ending_time = cleaned_data.get("ending_time")

        if starting_time and ending_time and starting_time >= ending_time:
            raise ValidationError("Starting time must be earlier than ending time.")

        return cleaned_data
