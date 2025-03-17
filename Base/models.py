from django.db import models
from Accounts.models import CustomUser
from datetime import timedelta


# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=100)
    trainer_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "trainer"},
        related_name="trainer_class",
    )
    start_date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()

    def __str__(self):
        return self.class_name

    def get_duration(self):
        start = timedelta(
            hours=self.starting_time.hour, minutes=self.starting_time.minute
        )
        end = timedelta(hours=self.ending_time.hour, minutes=self.ending_time.minute)
        duration = end - start
        return duration


class Booking(models.Model):
    client_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "member"},
        related_name="client_name",
    )
    trainer_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "trainer"},
        related_name="trainer_name",
    )
    class_name = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    

    def __str__(self):
        return self.name


class Membership(models.Model):
    membership_type = (
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("annually", "Annually"),
    )
    client_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "member"}
    )
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    membership_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
