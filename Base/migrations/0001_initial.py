# Generated by Django 5.1.6 on 2025-03-21 10:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('starting_time', models.TimeField()),
                ('ending_time', models.TimeField()),
                ('trainer_name', models.ForeignKey(limit_choices_to={'user_type': 'trainer'}, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_class', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.ForeignKey(limit_choices_to={'user_type': 'member'}, on_delete=django.db.models.deletion.CASCADE, related_name='client_name', to=settings.AUTH_USER_MODEL)),
                ('trainer_name', models.ForeignKey(limit_choices_to={'user_type': 'trainer'}, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_name', to=settings.AUTH_USER_MODEL)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='Base.class')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.FloatField()),
                ('membership_type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('client_name', models.ForeignKey(limit_choices_to={'user_type': 'member'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
