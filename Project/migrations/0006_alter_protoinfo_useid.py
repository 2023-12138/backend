# Generated by Django 4.2.4 on 2023-08-31 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Project", "0005_remove_protoinfo_use_protoinfo_useid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protoinfo",
            name="useid",
            field=models.IntegerField(default=-1, verbose_name="useid"),
        ),
    ]