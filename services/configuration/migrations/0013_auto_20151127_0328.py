# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0012_auto_20151125_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilityrule',
            name='ending_date',
            field=models.DateField(verbose_name='Ending date for the period'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityrule',
            name='operation',
            field=models.CharField(max_length=1, verbose_name='Rule operation', choices=[('+', 'Operation for adding new slots'), ('-', 'Operation for removing existing slots')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityrule',
            name='periodicity',
            field=models.CharField(max_length=1, verbose_name='Rule periodicity', choices=[('O', 'Rule that occurs only once.'), ('D', 'Rule that defines daily repetition pattern.'), ('W', 'Rule that defines a weekly repetition pattern.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityrule',
            name='starting_date',
            field=models.DateField(verbose_name='Starting date for the period'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruleonce',
            name='ending_time',
            field=models.DateTimeField(verbose_name='Ending datetime for the rule', default=django.utils.timezone.now, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruleonce',
            name='starting_time',
            field=models.DateTimeField(verbose_name='Starting datetime for the rule', default=django.utils.timezone.now, null=True),
            preserve_default=True,
        ),
    ]
