# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0006_auto_20151220_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundtrack',
            name='timestamp',
            field=djorm_pgarray.fields.BigIntegerArrayField(dbtype='bigint', verbose_name='UTC time at which the spacecraft is going to pass over'),
            preserve_default=True,
        ),
    ]
