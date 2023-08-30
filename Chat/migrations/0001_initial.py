# Generated by Django 4.2.4 on 2023-08-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chatroom",
            fields=[
                (
                    "cid",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="cid"
                    ),
                ),
                (
                    "cname",
                    models.CharField(
                        default="FusionChat", max_length=256, verbose_name="cname"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChatUser",
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
                ("cid", models.IntegerField(verbose_name="cid")),
                ("from_uid", models.IntegerField(null=True, verbose_name="from_uid")),
                ("to_uid", models.IntegerField(null=True, verbose_name="to_uid")),
                ("tid", models.IntegerField(null=True, verbose_name="tid")),
            ],
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "rid",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="rid"
                    ),
                ),
                ("cid", models.IntegerField(verbose_name="cid")),
                ("time", models.DateTimeField(auto_now_add=True, verbose_name="time")),
                ("content", models.TextField(max_length=1024, verbose_name="content")),
                ("sender", models.IntegerField(null=True, verbose_name="sender")),
                ("uid", models.IntegerField(null=True, verbose_name="uid")),
                ("tid", models.IntegerField(null=True, verbose_name="tid")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
            ],
        ),
    ]
