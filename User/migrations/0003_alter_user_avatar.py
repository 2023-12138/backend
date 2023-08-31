# Generated by Django 4.2.4 on 2023-08-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("User", "0002_user_authorid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.TextField(
                default="data:image/jpeg;base64,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",
                verbose_name="avatar",
            ),
        ),
    ]
