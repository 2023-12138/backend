# Generated by Django 4.2.4 on 2023-08-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prototype",
            fields=[
                (
                    "protoid",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="protoid"
                    ),
                ),
                ("pid", models.IntegerField(verbose_name="pid")),
                (
                    "protoname",
                    models.CharField(max_length=25, verbose_name="protoname"),
                ),
                ("info", models.JSONField(verbose_name="info")),
            ],
        ),
    ]
