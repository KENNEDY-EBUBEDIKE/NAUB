# Generated by Django 3.1.5 on 2021-08-08 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_auto_20210319_1744'),
        ('exams', '0011_auto_20210311_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationrequest',
            name='invigilators',
            field=models.ManyToManyField(related_name='examination_invigilator', to='staff.StaffProfile'),
        ),
    ]
