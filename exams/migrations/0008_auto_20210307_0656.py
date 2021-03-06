# Generated by Django 3.1.5 on 2021-03-07 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20210303_1443'),
        ('staff', '0003_auto_20210303_1443'),
        ('exams', '0007_examinationrequest_invigilators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancesheet',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_attendance_sheet', to='students.course'),
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance_sheet', to='students.studentprofile'),
        ),
        migrations.CreateModel(
            name='InvigilatorAttendanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_in_time', models.DateTimeField(auto_now_add=True)),
                ('sign_out_time', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invigilator_attendance_sheet', to='students.course')),
                ('invigilator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invigilator_attendance_sheet', to='staff.staffprofile')),
            ],
            options={
                'ordering': ('course',),
            },
        ),
    ]
