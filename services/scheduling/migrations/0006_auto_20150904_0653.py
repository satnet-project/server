# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0002_auto_20150212_0028'),
        ('scheduling', '0005_auto_20150903_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationalslot',
            name='pass_slot',
            field=models.ForeignKey(default=1, verbose_name='Pass slots related with this OperationalSlot', to='simulation.PassSlots'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operationalslot',
            name='availability_slot',
            field=models.ForeignKey(default=1, verbose_name='Availability slot related with this OperationalSlot', to='scheduling.AvailabilitySlot'),
            preserve_default=True,
        ),
    ]
