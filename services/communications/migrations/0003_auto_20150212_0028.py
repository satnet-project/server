# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communications', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='forwarded',
            field=models.BooleanField(default=False, verbose_name='Whether this message has already been forwarded to the receiver'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='groundstation_channel',
            field=models.ForeignKey(to='configuration.GroundStationChannel', verbose_name='GroundStation channel that tx/rx this message'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.BinaryField(verbose_name='Message raw data'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='operational_slot',
            field=models.ForeignKey(to='scheduling.OperationalSlot', verbose_name='OperationalSlot during which the message was transmitted'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='reception_timestamp',
            field=models.BigIntegerField(verbose_name='Timestamp at which this message was received at the server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='spacecraft_channel',
            field=models.ForeignKey(to='configuration.SpacecraftChannel', verbose_name='Spacecraft channel that tx/rx this message'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='transmission_timestamp',
            field=models.BigIntegerField(verbose_name='Timestamp at which this message was forwarded to the receiver'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='upwards',
            field=models.BooleanField(default=False, verbose_name='Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='doppler_shift',
            field=models.FloatField(verbose_name='Doppler shift during the reception of the message.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='groundstation',
            field=models.ForeignKey(to='configuration.GroundStation', verbose_name='GroundStation that tx/rx this message'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='groundstation_timestamp',
            field=models.BigIntegerField(verbose_name='Timestamp for when this message was received at the Ground Station'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='message',
            field=models.CharField(max_length=4000, verbose_name='Message raw data in base64'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='reception_timestamp',
            field=models.BigIntegerField(verbose_name='Timestamp for when this message was received at the server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passivemessage',
            name='retrieved',
            field=models.BooleanField(default=False, verbose_name='Indicates whether the message has been retrieved by a remote user.'),
            preserve_default=True,
        ),
    ]
