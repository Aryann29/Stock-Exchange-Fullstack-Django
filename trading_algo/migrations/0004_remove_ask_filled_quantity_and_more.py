# Generated by Django 5.0.2 on 2024-02-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trading_algo", "0003_ask_filled_quantity_bid_filled_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ask",
            name="filled_quantity",
        ),
        migrations.RemoveField(
            model_name="bid",
            name="filled_quantity",
        ),
        migrations.AddField(
            model_name="ask",
            name="total_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="bid",
            name="total_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
