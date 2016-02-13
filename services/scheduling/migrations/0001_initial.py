# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0001_initial'),
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(unique=True, max_length=100, verbose_name='Unique identifier for this slot')),
                ('start', models.DateTimeField(verbose_name='Slot start')),
                ('end', models.DateTimeField(verbose_name='Slot end')),
                ('groundstation', models.ForeignKey(verbose_name='GroundStation that this slot belongs to', default=1, to='configuration.GroundStation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChannelCompatibility',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('groundstation', models.ForeignKey(verbose_name='Reference to the compatible GroundStation segment', default=1, to='configuration.GroundStation')),
                ('groundstation_channel', models.ForeignKey(verbose_name='Reference to the compatible Ground Station channel', default=1, to='configuration.GroundStationChannel')),
                ('spacecraft', models.ForeignKey(verbose_name='Reference to the compatible Spacecraft segment', default=1, to='configuration.Spacecraft')),
                ('spacecraft_channel', models.ForeignKey(verbose_name='Reference to the compatible Spacecraft channel', default=1, to='configuration.SpacecraftChannel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OperationalSlot',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(unique=True, max_length=150, verbose_name='Unique identifier for this slot')),
                ('start', models.DateTimeField(verbose_name='Slot start')),
                ('end', models.DateTimeField(verbose_name='Slot end')),
                ('state', models.CharField(verbose_name='String that indicates the current state of the slot', max_length=10, choices=[('FREE', 'Slot not assigned for operation'), ('SELECTED', 'Slot chosen for reservation'), ('RESERVED', 'Slot confirmed by GroundStation'), ('DENIED', 'Slot petition denied'), ('CANCELED', 'Slot reservation canceled'), ('REMOVED', 'Slot removed due to a policy change')], default='FREE')),
                ('availability_slot', models.ForeignKey(verbose_name='Availability slot related with this OperationalSlot', default=1, to='scheduling.AvailabilitySlot')),
                ('pass_slot', models.ForeignKey(verbose_name='Pass slots related with this OperationalSlot', default=1, to='simulation.PassSlots')),
            ],
            options={
                'ordering': ['identifier'],
            },
            bases=(models.Model,),
        ),
    ]
