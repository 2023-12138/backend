# Generated by Django 4.2.4 on 2023-08-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notice",
            fields=[
                (
                    "noticeId",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="nid"
                    ),
                ),
                ("uid", models.IntegerField(verbose_name="uid")),
                ("rid", models.IntegerField(verbose_name="rid")),
                ("tid", models.IntegerField(null=True, verbose_name="tid")),
                ("docId", models.IntegerField(null=True, verbose_name="docId")),
                ("type", models.CharField(max_length=25, verbose_name="type")),
                ("read", models.IntegerField(default=0, verbose_name="read")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
            ],
        ),
    ]
