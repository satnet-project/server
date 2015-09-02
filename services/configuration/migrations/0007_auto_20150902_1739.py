# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_auto_20150902_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupedavailabilityrules',
            name='groundstation',
        ),
        migrations.RemoveField(
            model_name='groupedavailabilityrules',
            name='rules',
        ),
        migrations.DeleteModel(
            name='GroupedAvailabilityRules',
        ),
        migrations.RemoveField(
            model_name='availabilityrule',
            name='gs_channel',
        ),
        migrations.AddField(
            model_name='availabilityrule',
            name='groundstation',
            field=models.ForeignKey(to='configuration.GroundStation', default=1, verbose_name='Reference to the Ground Station that owns this rule'),
            preserve_default=True,
        ),
    ]
