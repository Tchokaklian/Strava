# Generated by Django 4.2 on 2023-11-20 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0045_remove_col_counter_year_col_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='col_counter',
            name='year_col_count',
            field=models.IntegerField(default=0),
        ),
    ]
