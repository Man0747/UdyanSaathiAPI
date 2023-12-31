# Generated by Django 4.2.6 on 2023-12-17 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AqiCalendarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(default=' ', max_length=255)),
                ('AQI', models.IntegerField(default=0)),
                ('Pol_Date', models.DateField(default='2023-10-10')),
            ],
        ),
        migrations.CreateModel(
            name='graphDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(default=' ', max_length=255)),
                ('AQI', models.IntegerField(default=0)),
                ('PM25', models.FloatField(default=0, max_length=10)),
                ('PM10', models.FloatField(default=0, max_length=10)),
                ('CO', models.FloatField(default=0, max_length=10)),
                ('OZONE', models.FloatField(default=0, max_length=10)),
                ('SO2', models.FloatField(default=0, max_length=10)),
                ('NO2', models.FloatField(default=0, max_length=10)),
                ('NH3', models.FloatField(default=0, max_length=10)),
                ('Pol_Date', models.DateField(default='2023-10-10')),
            ],
        ),
        migrations.CreateModel(
            name='pollutionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('State', models.CharField(default=' ', max_length=255)),
                ('City', models.CharField(default=' ', max_length=255)),
                ('Station', models.CharField(default=' ', max_length=500)),
                ('Pol_Date', models.DateTimeField(default=datetime.datetime(2023, 10, 10, 23, 0))),
                ('CO', models.FloatField(default=0, max_length=10)),
                ('NH3', models.FloatField(default=0, max_length=10)),
                ('NO2', models.FloatField(default=0, max_length=10)),
                ('OZONE', models.FloatField(default=0, max_length=10)),
                ('PM25', models.FloatField(default=0, max_length=10)),
                ('PM10', models.FloatField(default=0, max_length=10)),
                ('SO2', models.FloatField(default=0, max_length=10)),
                ('Checks', models.IntegerField(default=0)),
                ('AQI', models.IntegerField(default=0)),
                ('AQI_Quality', models.CharField(default=' ', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='stationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Station', models.CharField(default=' ', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Top10CitiesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(default=' ', max_length=255)),
                ('AQI', models.IntegerField(default=0)),
                ('PM25', models.FloatField(default=0, max_length=10)),
                ('PM10', models.FloatField(default=0, max_length=10)),
                ('CO', models.FloatField(default=0, max_length=10)),
                ('OZONE', models.FloatField(default=0, max_length=10)),
                ('SO2', models.FloatField(default=0, max_length=10)),
                ('NO2', models.FloatField(default=0, max_length=10)),
                ('NH3', models.FloatField(default=0, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Top10LeastCitiesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(default=' ', max_length=255)),
                ('AQI', models.IntegerField(default=0)),
                ('PM25', models.FloatField(default=0, max_length=10)),
                ('PM10', models.FloatField(default=0, max_length=10)),
                ('CO', models.FloatField(default=0, max_length=10)),
                ('OZONE', models.FloatField(default=0, max_length=10)),
                ('SO2', models.FloatField(default=0, max_length=10)),
                ('NO2', models.FloatField(default=0, max_length=10)),
                ('NH3', models.FloatField(default=0, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TopMetroCitiesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(default=' ', max_length=255)),
                ('AQI', models.IntegerField(default=0)),
                ('PM25', models.FloatField(default=0, max_length=10)),
                ('PM10', models.FloatField(default=0, max_length=10)),
                ('CO', models.FloatField(default=0, max_length=10)),
                ('OZONE', models.FloatField(default=0, max_length=10)),
                ('SO2', models.FloatField(default=0, max_length=10)),
                ('NO2', models.FloatField(default=0, max_length=10)),
                ('NH3', models.FloatField(default=0, max_length=10)),
            ],
        ),
    ]
