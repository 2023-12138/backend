# Generated by Django 4.2.4 on 2023-08-28 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Chat", "0004_record_tid_record_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="cid",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="cid"
            ),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="cname",
            field=models.CharField(
                default="FusionChat", max_length=256, verbose_name="cname"
            ),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="is_active"),
        ),
        migrations.AlterField(
            model_name="chatuser",
            name="cid",
            field=models.IntegerField(verbose_name="cid"),
        ),
        migrations.AlterField(
            model_name="chatuser",
            name="from_uid",
            field=models.IntegerField(null=True, verbose_name="from_uid"),
        ),
        migrations.AlterField(
            model_name="chatuser",
            name="tid",
            field=models.IntegerField(null=True, verbose_name="tid"),
        ),
        migrations.AlterField(
            model_name="chatuser",
            name="to_uid",
            field=models.IntegerField(null=True, verbose_name="to_uid"),
        ),
        migrations.AlterField(
            model_name="record",
            name="cid",
            field=models.IntegerField(verbose_name="cid"),
        ),
        migrations.AlterField(
            model_name="record",
            name="content",
            field=models.TextField(max_length=1024, verbose_name="content"),
        ),
        migrations.AlterField(
            model_name="record",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="is_active"),
        ),
        migrations.AlterField(
            model_name="record",
            name="rid",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="rid"
            ),
        ),
        migrations.AlterField(
            model_name="record",
            name="sender",
            field=models.IntegerField(null=True, verbose_name="sender"),
        ),
        migrations.AlterField(
            model_name="record",
            name="tid",
            field=models.IntegerField(null=True, verbose_name="tid"),
        ),
        migrations.AlterField(
            model_name="record",
            name="time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="record",
            name="uid",
            field=models.IntegerField(null=True, verbose_name="uid"),
        ),
    ]
