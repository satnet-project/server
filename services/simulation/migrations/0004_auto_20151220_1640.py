# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0003_auto_20151220_1639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passslots',
            options={'get_latest_by': ['start'], 'ordering': ['start']},
        ),
    ]
