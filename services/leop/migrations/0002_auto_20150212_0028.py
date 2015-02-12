# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('leop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifiedobject',
            name='identifier',
            field=models.PositiveSmallIntegerField(verbose_name='Object identifier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='identifiedobject',
            name='spacecraft',
            field=models.ForeignKey(to='configuration.Spacecraft', verbose_name='Spacecraft that represents this object'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='admin',
            field=models.ForeignKey(to='accounts.UserProfile', verbose_name='Administrator for this LEOP'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='cluster_spacecraft_id',
            field=models.CharField(unique=True, max_length=30, verbose_name='Cluster spacecraft identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_spacecraft_identifier')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='date',
            field=models.DateTimeField(verbose_name='Launch date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='groundstations',
            field=models.ManyToManyField(to='configuration.GroundStation', verbose_name='LEOP ground stations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='identified_objects',
            field=models.ManyToManyField(to='leop.IdentifiedObject', verbose_name='Object identified from within the cluster'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='identifier',
            field=models.CharField(unique=True, max_length=30, verbose_name='LEOP identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_leop_identifier')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='tle',
            field=models.ForeignKey(to='configuration.TwoLineElement', verbose_name='TLE for the cluster of objects as a whole'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='launch',
            name='unknown_objects',
            field=models.ManyToManyField(to='leop.UnknownObject', verbose_name='Objects still unknown'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unknownobject',
            name='identifier',
            field=models.PositiveSmallIntegerField(verbose_name='Object identifier'),
            preserve_default=True,
        ),
    ]
