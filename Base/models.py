from django.db import models
from Accounts.models import CustomUser
from datetime import timedelta, date
from django.utils import timezone
from django.core.exceptions import ValidationError


class Class(models.Model):
    DAYS_OF_WEEK = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    class_name = models.CharField(max_length=100)
    trainer_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "trainer"},
        related_name="trainer_class",
    )
    day_of_week = models.CharField(
        max_length=10, choices=DAYS_OF_WEEK, default="Monday"
    )
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
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.class_name}"

    @classmethod
    def register_member(cls, member, class_instance):
        # Check if the member has an active membership
        active_membership = Membership.objects.filter(
            client_name=member,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).exists()

        if not active_membership:
            raise ValidationError("You must have an active membership to book a class.")

        # Check if the member has already booked the same class on the same day
        existing_booking = cls.objects.filter(
            client_name=member,
            class_name=class_instance,
            booking_date=timezone.now().date(),
        ).exists()

        if existing_booking:
            raise ValidationError("You have already booked this class today.")

        booking = cls.objects.create(
            client_name=member,
            trainer_name=class_instance.trainer_name,
            class_name=class_instance,
        )
        return booking

    @staticmethod
    def is_booking_allowed(user, class_instance):
        active_membership = Membership.objects.filter(
            client_name=user,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).exists()
        return active_membership


class Membership(models.Model):
    MEMBERSHIP_TYPE_CHOICES = (
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    )
    MEMBERSHIP_PRICES = {
        "weekly": 2000,
        "monthly": 7500,
    }

    client_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "member"}
    )
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES)
    status = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.price = self.MEMBERSHIP_PRICES[self.membership_type]
        if self.membership_type == "weekly":
            self.end_date = self.start_date + timedelta(weeks=1)
        elif self.membership_type == "monthly":
            self.end_date = self.start_date + timedelta(weeks=4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_name} - {self.membership_type}"

    @classmethod
    def create_membership(cls, user, membership_type, start_date):
        end_date = (
            start_date + timedelta(weeks=1)
            if membership_type == "weekly"
            else start_date + timedelta(weeks=4)
        )
        membership = cls.objects.create(
            client_name=user,
            membership_type=membership_type,
            start_date=start_date,
            end_date=end_date,
            price=cls.MEMBERSHIP_PRICES[membership_type],
            status="active",
        )
        return membership
