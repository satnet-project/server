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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_sw_client', models.BooleanField(verbose_name='Defines whether this client is a remote software application or not', default=False)),
                ('user', models.ForeignKey(verbose_name='Reference to the profile of the user', to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_me', models.BooleanField(verbose_name='Flag that defines whether this object represents the current server', default=False)),
                ('is_external', models.BooleanField(verbose_name='Flag that defines whether this server belongs to this subnetwork', default=False)),
                ('identifier', models.CharField(unique=True, max_length=75, verbose_name='Identifier of the server as an element of the network', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_server_identifier')])),
                ('ip_address', models.IPAddressField(verbose_name='IP address of this network server')),
                ('latitude', models.FloatField(verbose_name='Latitude for the estimated position of this server')),
                ('longitude', models.FloatField(verbose_name='Longitude for the estimated position of this server')),
                ('timestamp', models.BigIntegerField(verbose_name='UTC time (in microseconds) of the last position estimation')),
                ('groundstations', models.ManyToManyField(verbose_name='Ground stations', to='configuration.GroundStation')),
                ('owner', models.ForeignKey(verbose_name='Owner of this network server', to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
