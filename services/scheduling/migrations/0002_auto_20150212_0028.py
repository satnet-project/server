# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationalslot',
            name='availability_slot',
            field=models.ForeignKey(to='configuration.AvailabilitySlot', on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='Availability slot that generates this OperationalSlot', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='end',
            field=models.DateTimeField(verbose_name='Slot end'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='groundstation_channel',
            field=models.ForeignKey(to='configuration.GroundStationChannel', on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='GroundStationChannel that this slot belongs to', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='gs_notified',
            field=models.BooleanField(default=False, verbose_name='Flag that indicates whether the changes in the status of the slot need already to be notified to the compatible GroundStation.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='identifier',
            field=models.CharField(unique=True, max_length=150, verbose_name='Unique identifier for this slot'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='sc_notified',
            field=models.BooleanField(default=False, verbose_name='Flag that indicates whether the changes in the status of the slot need already to be notified to the compatible Spacecraft.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='spacecraft_channel',
            field=models.ForeignKey(to='configuration.SpacecraftChannel', on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='SpacecraftChannel that this slot belongs to', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='start',
            field=models.DateTimeField(verbose_name='Slot start'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='state',
            field=models.CharField(default='FREE', max_length=10, verbose_name='String that indicates the current state of the slot', choices=[('FREE', 'Slot not assigned for operation'), ('SELECTED', 'Slot chosen for reservation'), ('RESERVED', 'Slot confirmed by GroundStation'), ('DENIED', 'Slot petition denied'), ('CANCELED', 'Slot reservation canceled'), ('REMOVED', 'Slot removed due to a policy change')]),
            preserve_default=True,
        ),
    ]
