# Generated by Django 3.1.5 on 2021-03-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20210314_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='id_number',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]