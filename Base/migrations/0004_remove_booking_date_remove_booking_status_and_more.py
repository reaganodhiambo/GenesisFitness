# Generated by Django 4.2.20 on 2025-03-17 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0003_rename_time_class_ending_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time',
        ),
        migrations.AlterField(
            model_name='booking',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='Base.class'),
        ),
    ]
