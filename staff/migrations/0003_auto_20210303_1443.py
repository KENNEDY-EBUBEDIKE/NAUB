# Generated by Django 3.1.5 on 2021-03-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_auto_20210227_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='rfid_code',
            field=models.BigIntegerField(blank=True, default=None, null=True, unique=True),
        ),
    ]
