# Generated by Django 3.1.5 on 2021-03-11 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20210303_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='rfid_code',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, unique=True),
        ),
    ]