from django import forms
from .models import *


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


class BookClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ["class_name", "trainer_name", "start_date", "starting_time", "ending_time"]
        widgets = {
            "members": forms.CheckboxSelectMultiple(),
        }
