# Generated by Django 4.2.4 on 2023-09-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("User", "0004_user_logincnt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.CharField(
                default="http://rzyi06q9n.hb-bkt.clouddn.com/%E4%BA%BA%E5%83%8F.png",
                max_length=255,
                verbose_name="avatar",
            ),
        ),
    ]
