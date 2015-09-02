# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_auto_20150902_0651'),
        ('scheduling', '0003_auto_20150831_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelCompatibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groundstation_channel', models.ForeignKey(to='configuration.GroundStationChannel', default=1, verbose_name='Reference to the compatible Ground Station channel')),
                ('spacecraft_channel', models.ForeignKey(to='configuration.SpacecraftChannel', default=1, verbose_name='Reference to the compatible Spacecraft channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='operationalslot',
            name='groundstation_channel',
        ),
        migrations.RemoveField(
            model_name='operationalslot',
            name='spacecraft_channel',
        ),
        migrations.AddField(
            model_name='operationalslot',
            name='compatible_channels',
            field=models.ForeignKey(to='scheduling.ChannelCompatibility', default=1, verbose_name='Reference to the compatible pair of channels'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='availability_slot',
            field=models.ForeignKey(to='configuration.AvailabilitySlot', default=1, verbose_name='Availability slot that generates this OperationalSlot'),
            preserve_default=True,
        ),
    ]
