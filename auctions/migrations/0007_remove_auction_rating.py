# Generated by Django 5.1.7 on 2025-05-09 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_alter_bid_bidder"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auction",
            name="rating",
        ),
    ]
