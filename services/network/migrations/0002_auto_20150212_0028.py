# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='is_sw_client',
            field=models.BooleanField(default=False, verbose_name='Defines whether this client is a remote software application or not'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.ForeignKey(to='accounts.UserProfile', verbose_name='Reference to the profile of the user'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='groundstations',
            field=models.ManyToManyField(to='configuration.GroundStation', verbose_name='LEOP ground stations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='identifier',
            field=models.CharField(unique=True, max_length=30, verbose_name='LEOP identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_leop_identifier')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='ip_address',
            field=models.IPAddressField(verbose_name='IP address of this network server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='is_external',
            field=models.BooleanField(default=False, verbose_name='Flag that defines whether this server belongs to this subnetwork'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='is_me',
            field=models.BooleanField(default=False, verbose_name='Flag that defines whether this object represents the current server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='latitude',
            field=models.FloatField(verbose_name='Latitude for the estimated position of this server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='longitude',
            field=models.FloatField(verbose_name='Longitude for the estimated position of this server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='owner',
            field=models.ForeignKey(to='accounts.UserProfile', verbose_name='Owner of this network server'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='timestamp',
            field=models.BigIntegerField(verbose_name='UTC time (in microseconds) of the last position estimation'),
            preserve_default=True,
        ),
    ]
