# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0014_auto_20151127_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityrule',
            name='ending_date',
        ),
        migrations.RemoveField(
            model_name='availabilityrule',
            name='starting_date',
        ),
    ]
