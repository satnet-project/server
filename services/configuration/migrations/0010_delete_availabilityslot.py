# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_auto_20150903_1840'),
        ('configuration', '0009_remove_availabilityslot_groundstation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AvailabilitySlot',
        ),
    ]
