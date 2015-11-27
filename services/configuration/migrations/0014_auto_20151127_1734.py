# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0013_auto_20151127_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilityrule',
            name='ending_date',
            field=models.DateField(null=True, verbose_name='Ending date for the applicability period of the rule', default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityrule',
            name='starting_date',
            field=models.DateField(null=True, verbose_name='Starting date for the applicability period of the rule', default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
