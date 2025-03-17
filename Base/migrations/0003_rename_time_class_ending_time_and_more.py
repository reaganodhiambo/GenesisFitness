# Generated by Django 4.2.20 on 2025-03-16 23:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='time',
            new_name='ending_time',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='date',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='class',
            name='status',
        ),
        migrations.AddField(
            model_name='class',
            name='starting_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
