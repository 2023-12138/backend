# Generated by Django 4.1.2 on 2023-08-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("User", "0003_user_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="identity",
            field=models.IntegerField(default=0, verbose_name="identity"),
        ),
    ]