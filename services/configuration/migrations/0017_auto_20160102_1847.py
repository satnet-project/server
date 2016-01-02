# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0016_auto_20151127_1735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='twolineelement',
            options={'ordering': ['identifier']},
        ),
    ]
