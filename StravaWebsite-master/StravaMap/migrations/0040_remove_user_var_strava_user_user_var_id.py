# Generated by Django 4.2 on 2023-11-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0039_remove_user_dashboard_strava_user_user_dashboard_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_var',
            name='strava_user',
        ),
        migrations.AddField(
            model_name='user_var',
            name='id',
            field=models.IntegerField(auto_created=True, default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
