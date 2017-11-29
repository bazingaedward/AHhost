# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ahhost', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='province',
            name='ID',
            field=models.CharField(serialize=False, max_length=50, default=1, primary_key=True, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
