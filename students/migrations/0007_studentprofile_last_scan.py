# Generated by Django 3.1.5 on 2021-02-20 09:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20210220_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='last_scan',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]