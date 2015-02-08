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
            name='IdentifiedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.PositiveSmallIntegerField(verbose_name=b'Object identifier')),
                ('spacecraft', models.ForeignKey(verbose_name=b'Spacecraft that represents this object', to='configuration.Spacecraft')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'LEOP identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_leop_identifier')])),
                ('date', models.DateTimeField(verbose_name=b'Launch date')),
                ('cluster_spacecraft_id', models.CharField(unique=True, max_length=30, verbose_name=b'Cluster spacecraft identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_spacecraft_identifier')])),
                ('admin', models.ForeignKey(verbose_name=b'Administrator for this LEOP', to='accounts.UserProfile')),
                ('groundstations', models.ManyToManyField(to='configuration.GroundStation', verbose_name=b'LEOP ground stations')),
                ('identified_objects', models.ManyToManyField(to='leop.IdentifiedObject', verbose_name=b'Object identified from within the cluster')),
                ('tle', models.ForeignKey(verbose_name=b'TLE for the cluster of objects as a whole', to='configuration.TwoLineElement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnknownObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.PositiveSmallIntegerField(verbose_name=b'Object identifier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='launch',
            name='unknown_objects',
            field=models.ManyToManyField(to='leop.UnknownObject', verbose_name=b'Objects still unknown'),
            preserve_default=True,
        ),
    ]
