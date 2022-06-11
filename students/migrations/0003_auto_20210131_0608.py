# Generated by Django 3.1.5 on 2021-01-31 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20210129_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_name',
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_title',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
