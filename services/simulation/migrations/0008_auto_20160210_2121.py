# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0007_auto_20160102_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundtrack',
            name='latitude',
            field=models.TextField(max_length=10000000, default='', verbose_name='List of latitudes in a comma separated value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='longitude',
            field=models.TextField(max_length=10000000, default='', verbose_name='List of longitudes in a comma separated value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='timestamp',
            field=models.TextField(max_length=10000000, default='', verbose_name='List of timestamps in a comma separated value'),
            preserve_default=True,
        ),
    ]
