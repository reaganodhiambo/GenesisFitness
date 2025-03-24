from django.db import models
from Accounts.models import CustomUser
# Create your models here.


class TrainerProfile(models.Model):
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'trainer'}, related_name="trainer_profile")
    speciality = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
