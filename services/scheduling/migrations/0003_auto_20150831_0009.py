# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_auto_20150212_0028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operationalslot',
            options={'ordering': ['identifier']},
        ),
    ]
