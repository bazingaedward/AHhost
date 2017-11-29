# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('ID', models.CharField(max_length=50, serialize=False, primary_key=True, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('minx', models.FloatField()),
                ('miny', models.FloatField()),
                ('maxx', models.FloatField()),
                ('maxy', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PointSource',
            fields=[
                ('stationName', models.CharField(max_length=200, serialize=False, primary_key=True, unique=True)),
                ('areaId', models.CharField(max_length=10)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('county', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('industryId', models.CharField(max_length=10)),
                ('industryName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PointSourceData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('SO2', models.FloatField(null=True)),
                ('NOX', models.FloatField()),
                ('CO', models.FloatField()),
                ('PM', models.FloatField()),
                ('PM10', models.FloatField()),
                ('PM25', models.FloatField()),
                ('NMVOC', models.FloatField()),
                ('NH3', models.FloatField()),
                ('date', models.DateField()),
                ('station', models.ForeignKey(to='ahhost.PointSource')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True, unique=True)),
                ('minx', models.FloatField()),
                ('miny', models.FloatField()),
                ('maxx', models.FloatField()),
                ('maxy', models.FloatField()),
            ],
        ),
    ]
