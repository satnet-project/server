# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
        ('scheduling', '0001_initial'),
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upwards', models.BooleanField(default=False, verbose_name=b'Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)')),
                ('forwarded', models.BooleanField(default=False, verbose_name=b'Whether this message has already been forwarded to the receiver')),
                ('reception_timestamp', models.BigIntegerField(verbose_name=b'Timestamp at which this message was received at the server')),
                ('transmission_timestamp', models.BigIntegerField(verbose_name=b'Timestamp at which this message was forwarded to the receiver')),
                ('message', models.BinaryField(verbose_name=b'Message raw data')),
                ('groundstation_channel', models.ForeignKey(verbose_name=b'GroundStation channel that tx/rx this message', to='configuration.GroundStationChannel')),
                ('operational_slot', models.ForeignKey(verbose_name=b'OperationalSlot during which the message was transmitted', to='scheduling.OperationalSlot')),
                ('spacecraft_channel', models.ForeignKey(verbose_name=b'Spacecraft channel that tx/rx this message', to='configuration.SpacecraftChannel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
