# Generated by Django 3.1.5 on 2021-02-02 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20210202_0606'),
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancesheet',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_sheet', to='students.course'),
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_sheet', to='students.studentprofile'),
        ),
    ]
