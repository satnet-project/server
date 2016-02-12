# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communications', '0003_auto_20150212_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='groundstation_channel',
            field=models.ForeignKey(verbose_name='GroundStation channel that tx/rx this message', to='configuration.GroundStationChannel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='spacecraft_channel',
            field=models.ForeignKey(verbose_name='Spacecraft channel that tx/rx this message', to='configuration.SpacecraftChannel', null=True),
            preserve_default=True,
        ),
    ]
