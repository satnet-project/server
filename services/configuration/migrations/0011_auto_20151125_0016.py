# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_delete_availabilityslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabilityruledaily',
            name='ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruledaily',
            name='starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleonce',
            name='ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleonce',
            name='starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='friday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='friday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='monday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='monday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='saturday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='saturday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='sunday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='sunday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='thursday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='thursday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='tuesday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='tuesday_starting_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='wednesday_ending_time',
        ),
        migrations.RemoveField(
            model_name='availabilityruleweekly',
            name='wednesday_starting_time',
        ),
    ]
