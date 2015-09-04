# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0008_remove_operationalslot_compatible_channels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationalslot',
            name='gs_notified',
        ),
        migrations.RemoveField(
            model_name='operationalslot',
            name='sc_notified',
        ),
    ]
