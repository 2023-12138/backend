# Generated by Django 4.2.4 on 2023-09-02 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doc",
            fields=[
                (
                    "docId",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="docId"
                    ),
                ),
                ("pid", models.IntegerField(verbose_name="pid")),
                ("docname", models.CharField(max_length=25, verbose_name="docname")),
                ("padid", models.CharField(max_length=55, verbose_name="padid")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DocContent",
            fields=[
                (
                    "docContentId",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="docContentId"
                    ),
                ),
                ("docId", models.IntegerField(verbose_name="docId")),
                ("docContent", models.TextField(default="", verbose_name="docContent")),
                (
                    "saveTime",
                    models.DateTimeField(auto_now_add=True, verbose_name="saveTime"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is_active"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Session",
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
                ("groupid", models.CharField(max_length=55, verbose_name="groupid")),
                ("authorid", models.CharField(max_length=55, verbose_name="authorid")),
                (
                    "sessionid",
                    models.CharField(max_length=55, verbose_name="sessionid"),
                ),
            ],
        ),
    ]
