# Generated by Django 3.1.5 on 2021-08-12 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_scanrecords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanrecords',
            name='location',
            field=models.CharField(blank=True, default='T.Y Buratai Gate', max_length=50, null=True),
        ),
    ]
