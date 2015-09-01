# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_auto_20150831_0009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channelcompatibility',
            name='groundstation_channels',
        ),
        migrations.AddField(
            model_name='channelcompatibility',
            name='groundstation_channel',
            field=models.ForeignKey(verbose_name='Reference to the compatible Ground Station channel', default=1, to='configuration.GroundStationChannel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='channelcompatibility',
            name='spacecraft_channel',
            field=models.ForeignKey(verbose_name='Reference to the compatible Spacecraft channel', default=1, to='configuration.SpacecraftChannel'),
            preserve_default=True,
        ),
    ]
