# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_auto_20150212_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityrule',
            name='gs_channel',
        ),
        migrations.AddField(
            model_name='availabilityrule',
            name='ground_station',
            field=models.ForeignKey(to='configuration.GroundStation', verbose_name='Ground Station to which this rule belongs to', default=1),
            preserve_default=True,
        ),
    ]
