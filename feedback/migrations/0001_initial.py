# Generated by Django 5.1.4 on 2025-01-07 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("upload", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("accuracy", models.FloatField(blank=True, null=True)),
                ("syllables_per_second", models.FloatField(blank=True, null=True)),
                ("speed", models.CharField(blank=True, max_length=10, null=True)),
                ("um_count", models.IntegerField(default=0)),
                ("uh_count", models.IntegerField(default=0)),
                ("geu_count", models.IntegerField(default=0)),
                ("bad_gesture_count", models.IntegerField(default=0)),
                ("good_gesture_count", models.IntegerField(default=0)),
                ("standing_on_one_leg_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "upload",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedback",
                        to="upload.userupload",
                    ),
                ),
            ],
        ),
    ]
