# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_auto_20150714_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groundstation',
            name='channels',
        ),
        migrations.RemoveField(
            model_name='spacecraft',
            name='channels',
        ),
        migrations.AddField(
            model_name='groundstationchannel',
            name='groundstation',
            field=models.ForeignKey(to='configuration.GroundStation', default=1, verbose_name='Ground Station that this channel belongs to'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spacecraftchannel',
            name='spacecraft',
            field=models.ForeignKey(to='configuration.Spacecraft', default=1, verbose_name='Spacecraft that this channel belongs to'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundstationchannel',
            name='band',
            field=models.ForeignKey(to='configuration.AvailableBands', verbose_name='Band for the channel of the Ground Station'),
            preserve_default=True,
        ),
    ]
