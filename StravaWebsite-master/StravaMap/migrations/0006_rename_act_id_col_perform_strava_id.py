# Generated by Django 4.2 on 2023-05-31 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0005_remove_col_counter_col_id_remove_col_perform_col_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='col_perform',
            old_name='act_id',
            new_name='strava_id',
        ),
    ]
