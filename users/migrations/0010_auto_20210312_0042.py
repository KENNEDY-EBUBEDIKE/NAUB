# Generated by Django 3.1.5 on 2021-03-11 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210312_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codebase',
            name='rfid_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
