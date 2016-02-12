# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0009_auto_20150904_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationalslot',
            name='availability_slot',
            field=models.ForeignKey(verbose_name='Availability slot related with this OperationalSlot', to='scheduling.AvailabilitySlot', null=True),
            preserve_default=True,
        ),
    ]
