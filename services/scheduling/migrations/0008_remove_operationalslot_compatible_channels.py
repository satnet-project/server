# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0007_auto_20150904_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationalslot',
            name='compatible_channels',
        ),
    ]
