# Generated by Django 3.1.5 on 2021-01-28 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(blank=True, max_length=20, null=True)),
                ('course_name', models.CharField(blank=True, max_length=20, null=True)),
                ('course_title', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ('course_code',),
            },
        ),
        migrations.CreateModel(
            name='StudentsProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('surname', models.CharField(max_length=50, null=True)),
                ('other_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.BigIntegerField(default='+234', unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('rfid_code', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('matric_number', models.CharField(default='NAUB/', max_length=22, unique=True)),
                ('faculty', models.CharField(max_length=100, null=True)),
                ('department', models.CharField(max_length=100, null=True)),
                ('session', models.CharField(max_length=9, null=True)),
                ('level', models.TextField(null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('nationality', models.CharField(max_length=10, null=True)),
                ('state_of_origin', models.CharField(max_length=20, null=True)),
                ('lga', models.CharField(max_length=50, null=True)),
                ('resident_address', models.TextField(null=True)),
                ('photo', models.ImageField(null=True, upload_to='image/')),
                ('is_flaged', models.BooleanField(default=False, help_text='Designates whether this student is declared wanted.')),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('courses', models.ManyToManyField(to='students.Course')),
            ],
            options={
                'ordering': ('matric_number',),
            },
        ),
    ]
