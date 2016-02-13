# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('upwards', models.BooleanField(verbose_name='Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)', default=False)),
                ('forwarded', models.BooleanField(verbose_name='Whether this message has already been forwarded to the receiver', default=False)),
                ('reception_timestamp', models.BigIntegerField(verbose_name='Timestamp at which this message was received at the server')),
                ('transmission_timestamp', models.BigIntegerField(verbose_name='Timestamp at which this message was forwarded to the receiver')),
                ('message', models.BinaryField(verbose_name='Message raw data')),
                ('groundstation_channel', models.ForeignKey(verbose_name='GroundStation channel that tx/rx this message', to='configuration.GroundStationChannel')),
                ('operational_slot', models.ForeignKey(verbose_name='OperationalSlot during which the message was transmitted', to='scheduling.OperationalSlot')),
                ('spacecraft_channel', models.ForeignKey(verbose_name='Spacecraft channel that tx/rx this message', to='configuration.SpacecraftChannel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PassiveMessage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('retrieved', models.BooleanField(verbose_name='Indicates whether the message has been retrieved by a remote user.', default=False)),
                ('doppler_shift', models.FloatField(verbose_name='Doppler shift during the reception of the message.')),
                ('groundstation_timestamp', models.BigIntegerField(verbose_name='Timestamp for when this message was received at the Ground Station')),
                ('reception_timestamp', models.BigIntegerField(verbose_name='Timestamp for when this message was received at the server')),
                ('message', models.CharField(verbose_name='Message raw data in base64', max_length=4000)),
                ('groundstation', models.ForeignKey(verbose_name='GroundStation that tx/rx this message', to='configuration.GroundStation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
