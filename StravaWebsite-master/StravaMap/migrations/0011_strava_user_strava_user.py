# Generated by Django 4.2 on 2023-06-22 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0010_alter_strava_user_athlete_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='strava_user',
            name='strava_user',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
