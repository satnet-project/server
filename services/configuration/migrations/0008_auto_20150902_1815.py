# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_auto_20150902_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityslot',
            name='groundstation_channel',
        ),
        migrations.AddField(
            model_name='availabilityslot',
            name='groundstation',
            field=models.ForeignKey(verbose_name='GroundStation that this slot belongs to', default=1, to='configuration.GroundStation'),
            preserve_default=True,
        ),
    ]
