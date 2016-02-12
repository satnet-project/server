# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0010_auto_20160212_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationalslot',
            name='pass_slot',
            field=models.ForeignKey(null=True, verbose_name='Pass slots related with this OperationalSlot', to='simulation.PassSlots'),
            preserve_default=True,
        ),
    ]
