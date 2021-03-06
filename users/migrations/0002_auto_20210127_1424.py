# Generated by Django 3.1.5 on 2021-01-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='other_name',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lga',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state_of_origin',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
