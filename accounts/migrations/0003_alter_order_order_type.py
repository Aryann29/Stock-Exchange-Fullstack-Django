# Generated by Django 5.0.2 on 2024-02-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_order_order_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_type",
            field=models.CharField(
                choices=[("BID", "bid"), ("ASK", "ask")], max_length=3
            ),
        ),
    ]