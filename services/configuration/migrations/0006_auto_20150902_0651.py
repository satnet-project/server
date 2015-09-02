# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20150901_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channelcompatibility',
            name='groundstation_channel',
        ),
        migrations.RemoveField(
            model_name='channelcompatibility',
            name='spacecraft_channel',
        ),
        migrations.DeleteModel(
            name='ChannelCompatibility',
        ),
    ]
