# Generated by Django 4.1.2 on 2023-08-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chatroom",
            fields=[
                ("cid", models.AutoField(primary_key=True, serialize=False)),
                ("cname", models.CharField(max_length=256)),
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
                ("cid", models.IntegerField()),
                ("uid1", models.IntegerField(null=True)),
                ("uid2", models.IntegerField(null=True)),
                ("tid", models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                ("rid", models.AutoField(primary_key=True, serialize=False)),
                ("cid", models.IntegerField()),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("content", models.TextField(max_length=1024)),
                ("sender", models.IntegerField(null=True)),
            ],
        ),
    ]
