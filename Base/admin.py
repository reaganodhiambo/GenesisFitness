from django.contrib import admin
from .models import *


# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = [
        "class_name",
        "trainer_name",
        "day_of_week",
        "starting_time",
        "ending_time",
    ]
    list_filter = ["class_name", "day_of_week", "trainer_name"]


class BookingAdmin(admin.ModelAdmin):
    list_display = ["client_name", "trainer_name", "class_name"]
    list_filter = ["client_name", "trainer_name", "class_name"]


class MembershipAdmin(admin.ModelAdmin):
    list_display = ["membership_type", "start_date", "end_date"]
    list_filter = ["membership_type", "start_date", "end_date"]


admin.site.register(Booking)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Class, ClassAdmin)
