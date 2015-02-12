# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundtrack',
            name='latitude',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision', verbose_name='Latitude for the points of the GroundTrack'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='longitude',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision', verbose_name='Longitude for the points of the GroundTrack'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='spacecraft',
            field=models.ForeignKey(unique=True, to='configuration.Spacecraft', verbose_name='Reference to the Spacecraft that owns this GroundTrack'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='timestamp',
            field=djorm_pgarray.fields.BigIntegerArrayField(dbtype='bigint', verbose_name='UTC time at which the spacecraft is going to pass over this point'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groundtrack',
            name='tle',
            field=models.ForeignKey(to='configuration.TwoLineElement', verbose_name='Reference to the TLE object used for this GroundTrack'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passslots',
            name='end',
            field=models.DateTimeField(verbose_name='Slot end'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passslots',
            name='groundstation',
            field=models.ForeignKey(to='configuration.GroundStation', verbose_name='GroundStation linked to this pass'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passslots',
            name='spacecraft',
            field=models.ForeignKey(to='configuration.Spacecraft', verbose_name='Spacecraft linked to this pass'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='passslots',
            name='start',
            field=models.DateTimeField(verbose_name='Slot start'),
            preserve_default=True,
        ),
    ]
