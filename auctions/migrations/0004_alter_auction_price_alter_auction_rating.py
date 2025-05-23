# Generated by Django 5.1.7 on 2025-04-06 19:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_bid_options_alter_auction_stock"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="price",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="auction",
            name="rating",
            field=models.IntegerField(),
        ),
    ]
