# Generated by Django 4.2 on 2023-10-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StravaMap', '0026_delete_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col_count', models.IntegerField(null=True)),
            ],
        ),
    ]