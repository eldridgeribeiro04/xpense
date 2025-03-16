# Generated by Django 5.1.4 on 2025-03-16 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Money",
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
                ("total_money", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="ExpenseTracker",
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
                ("product", models.CharField(max_length=100)),
                ("product_count", models.PositiveIntegerField()),
                ("product_cost", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "money",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tracker.money"
                    ),
                ),
            ],
        ),
    ]
