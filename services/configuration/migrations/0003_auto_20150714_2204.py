# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_auto_20150212_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupedAvailabilityRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groundstation', models.ForeignKey(default=1, verbose_name='Reference to the Ground Station', to='configuration.GroundStation')),
                ('rules', models.ManyToManyField(verbose_name='Rules belonging to the same group', to='configuration.AvailabilityRule')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='availabilityrule',
            options={'ordering': ['id']},
        ),
    ]
