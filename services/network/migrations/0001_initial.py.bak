# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_sw_client', models.BooleanField(default=False, verbose_name=b'Defines whether this client is a remote software application or not')),
                ('user', models.ForeignKey(verbose_name=b'Reference to the profile of the user', to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_me', models.BooleanField(default=False, verbose_name=b'Flag that defines whether this object represents the current server')),
                ('is_external', models.BooleanField(default=False, verbose_name=b'Flag that defines whether this server belongs to this subnetwork')),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'LEOP identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_leop_identifier')])),
                ('ip_address', models.IPAddressField(verbose_name=b'IP address of this network server')),
                ('latitude', models.FloatField(verbose_name=b'Latitude for the estimated position of this server')),
                ('longitude', models.FloatField(verbose_name=b'Longitude for the estimated position of this server')),
                ('timestamp', models.BigIntegerField(verbose_name=b'UTC time (in microseconds) of the last position estimation')),
                ('groundstations', models.ManyToManyField(to='configuration.GroundStation', verbose_name=b'LEOP ground stations')),
                ('owner', models.ForeignKey(verbose_name=b'Owner of this network server', to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
