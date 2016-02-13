# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroundTrack',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('latitude', models.TextField(verbose_name='List of latitudes in a comma separated value', max_length=10000000, default='')),
                ('longitude', models.TextField(verbose_name='List of longitudes in a comma separated value', max_length=10000000, default='')),
                ('timestamp', models.TextField(verbose_name='List of timestamps in a comma separated value', max_length=10000000, default='')),
                ('spacecraft', models.ForeignKey(unique=True, verbose_name='Reference to the Spacecraft that owns this GroundTrack', to='configuration.Spacecraft')),
                ('tle', models.ForeignKey(verbose_name='Reference to the TLE object used for this GroundTrack', to='configuration.TwoLineElement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PassSlots',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField(verbose_name='Slot start')),
                ('end', models.DateTimeField(verbose_name='Slot end')),
                ('groundstation', models.ForeignKey(verbose_name='GroundStation linked to this pass', to='configuration.GroundStation')),
                ('spacecraft', models.ForeignKey(verbose_name='Spacecraft linked to this pass', to='configuration.Spacecraft')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
