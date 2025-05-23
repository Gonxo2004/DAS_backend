# Generated by Django 5.1.7 on 2025-05-10 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auctions", "0007_remove_auction_rating"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("title", models.CharField(max_length=50)),
                ("body", models.TextField()),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("last_modification_date", models.DateTimeField(auto_now=True)),
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="auctions.auction",
                    ),
                ),
                ("user", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
