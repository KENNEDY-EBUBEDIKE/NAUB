# Generated by Django 3.1.5 on 2021-08-09 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_course_credit_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScanRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_time', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scan_records', to='students.studentprofile')),
            ],
            options={
                'ordering': ('scan_time',),
            },
        ),
    ]