# Generated by Django 3.1.5 on 2021-02-28 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_remove_studentprofile_rfid_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='rfid_code',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
