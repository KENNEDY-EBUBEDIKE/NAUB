# Generated by Django 3.1.5 on 2021-03-07 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20210303_1443'),
        ('exams', '0009_auto_20210307_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationmalpractice',
            name='invigilator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_malpractice', to='staff.staffprofile'),
        ),
    ]