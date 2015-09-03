# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0008_auto_20150902_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityslot',
            name='groundstation',
        ),
    ]
