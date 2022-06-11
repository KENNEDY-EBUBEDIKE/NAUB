# Generated by Django 3.1.5 on 2021-02-28 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0006_auto_20210227_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codebase',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]