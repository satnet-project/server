# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroundTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', djorm_pgarray.fields.FloatArrayField(dbtype='double precision', verbose_name=b'Latitude for the points of the GroundTrack')),
                ('longitude', djorm_pgarray.fields.FloatArrayField(dbtype='double precision', verbose_name=b'Longitude for the points of the GroundTrack')),
                ('timestamp', djorm_pgarray.fields.BigIntegerArrayField(dbtype='bigint', verbose_name=b'UTC time at which the spacecraft is going to pass over this point')),
                ('spacecraft', models.ForeignKey(verbose_name=b'Reference to the Spacecraft that owns this GroundTrack', to='configuration.Spacecraft', unique=True)),
                ('tle', models.ForeignKey(verbose_name=b'Reference to the TLE object used for this GroundTrack', to='configuration.TwoLineElement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PassSlots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name=b'Slot start')),
                ('end', models.DateTimeField(verbose_name=b'Slot end')),
                ('groundstation', models.ForeignKey(verbose_name=b'GroundStation linked to this pass', to='configuration.GroundStation')),
                ('spacecraft', models.ForeignKey(verbose_name=b'Spacecraft linked to this pass', to='configuration.Spacecraft')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
