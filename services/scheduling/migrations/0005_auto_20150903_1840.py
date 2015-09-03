# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_remove_availabilityslot_groundstation'),
        ('scheduling', '0004_auto_20150902_0651'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('identifier', models.CharField(max_length=100, unique=True, verbose_name='Unique identifier for this slot')),
                ('start', models.DateTimeField(verbose_name='Slot start')),
                ('end', models.DateTimeField(verbose_name='Slot end')),
                ('groundstation', models.ForeignKey(to='configuration.GroundStation', default=1, verbose_name='GroundStation that this slot belongs to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='availability_slot',
            field=models.ForeignKey(to='scheduling.AvailabilitySlot', default=1, verbose_name='Availability slot that generates this OperationalSlot'),
            preserve_default=True,
        ),
    ]
