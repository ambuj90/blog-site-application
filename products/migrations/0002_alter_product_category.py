# Generated by Django 4.2.19 on 2025-03-12 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[("electronics", "Electronics"), ("clothing", "Clothing")],
                max_length=100,
            ),
        ),
    ]
