# Generated by Django 3.1.5 on 2021-01-31 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20210131_0608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='department',
            new_name='course_department',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='faculty',
            new_name='course_faculty',
        ),
    ]