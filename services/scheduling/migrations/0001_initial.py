# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationalSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=150, verbose_name=b'Unique identifier for this slot')),
                ('start', models.DateTimeField(verbose_name=b'Slot start')),
                ('end', models.DateTimeField(verbose_name=b'Slot end')),
                ('state', models.CharField(default='FREE', max_length=10, verbose_name=b'String that indicates the current state of the slot', choices=[('FREE', b'Slot not assigned for operation'), ('SELECTED', b'Slot chosen for reservation'), ('RESERVED', b'Slot confirmed by GroundStation'), ('DENIED', b'Slot petition denied'), ('CANCELED', b'Slot reservation canceled'), ('REMOVED', b'Slot removed due to a policy change')])),
                ('gs_notified', models.BooleanField(default=False, verbose_name=b'Flag that indicates whether the changes in the status of the slot need already to be notified to the compatible GroundStation.')),
                ('sc_notified', models.BooleanField(default=False, verbose_name=b'Flag that indicates whether the changes in the status of the slot need already to be notified to the compatible Spacecraft.')),
                ('availability_slot', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Availability slot that generates this OperationalSlot', blank=True, to='configuration.AvailabilitySlot', null=True)),
                ('groundstation_channel', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'GroundStationChannel that this slot belongs to', blank=True, to='configuration.GroundStationChannel', null=True)),
                ('spacecraft_channel', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'SpacecraftChannel that this slot belongs to', blank=True, to='configuration.SpacecraftChannel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
