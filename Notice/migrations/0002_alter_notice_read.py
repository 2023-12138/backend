# Generated by Django 4.2.4 on 2023-08-26 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Notice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="read",
            field=models.IntegerField(default=0, verbose_name="read"),
        ),
    ]
