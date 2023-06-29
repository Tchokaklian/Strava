# Generated by Django 4.2 on 2023-06-22 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0008_alter_col_counter_col_count_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strava_user',
            fields=[
                ('strava_user_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='-', max_length=100)),
                ('last_name', models.CharField(default='-', max_length=100)),
                ('token_type', models.CharField(default='-', max_length=100)),
                ('access_token', models.CharField(default='-', max_length=100)),
                ('refresh_token', models.CharField(default='-', max_length=100)),
                ('expire_at', models.DateTimeField()),
                ('athlete_id', models.IntegerField()),
                ('city', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('sex', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]