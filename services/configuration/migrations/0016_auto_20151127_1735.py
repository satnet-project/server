# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0015_auto_20151127_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabilityrule',
            name='ending_date',
            field=models.DateField(null=True, default=django.utils.timezone.now, verbose_name='Ending date for the applicability period of the rule'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityrule',
            name='starting_date',
            field=models.DateField(null=True, default=django.utils.timezone.now, verbose_name='Starting date for the applicability period of the rule'),
            preserve_default=True,
        ),
    ]
