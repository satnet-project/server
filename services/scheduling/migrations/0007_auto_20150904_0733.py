# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_delete_availabilityslot'),
        ('scheduling', '0006_auto_20150904_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelcompatibility',
            name='groundstation',
            field=models.ForeignKey(verbose_name='Reference to the compatible GroundStation segment', default=1, to='configuration.GroundStation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channelcompatibility',
            name='spacecraft',
            field=models.ForeignKey(verbose_name='Reference to the compatible Spacecraft segment', default=1, to='configuration.Spacecraft'),
            preserve_default=True,
        ),
    ]
