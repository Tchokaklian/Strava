# Generated by Django 4.2 on 2023-11-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0042_perform_strava_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_var',
            name='last_update',
            field=models.IntegerField(null=True),
        ),
    ]