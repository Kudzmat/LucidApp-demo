# Generated by Django 4.1.7 on 2025-06-10 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0003_alter_inventory_selling_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                (
                    "name",
                    models.CharField(
                        help_text="The name of the customer", max_length=255
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="The email address of the customer", max_length=254
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        default="N/A",
                        help_text="The address of the customer",
                        max_length=255,
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        help_text="The city of the customer",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        help_text="The country of the customer",
                        max_length=100,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.RemoveField(
            model_name="storepurchase",
            name="customer_address",
        ),
        migrations.RemoveField(
            model_name="storepurchase",
            name="customer_email",
        ),
        migrations.RemoveField(
            model_name="storepurchase",
            name="customer_name",
        ),
        migrations.AddField(
            model_name="storepurchase",
            name="customer_details",
            field=models.ForeignKey(
                default=None,
                help_text="The customer who made the purchase",
                on_delete=django.db.models.deletion.CASCADE,
                to="sales.customer",
            ),
        ),
    ]
