from django.contrib import admin
from .models import *
# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ["class_name", "trainer_name", "day_of_week", "starting_time", "ending_time"]
    list_filter = ["class_name","day_of_week", "trainer_name"]


admin.site.register(Booking)
admin.site.register(Membership)
admin.site.register(Class)