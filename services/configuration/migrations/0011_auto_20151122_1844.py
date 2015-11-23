# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_delete_availabilityslot'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='f_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Friday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='f_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Friday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='m_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Monday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='m_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Monday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='r_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Thursday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='r_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Thursday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='s_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Saturday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='s_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Saturday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='t_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Tuesday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='t_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Tuesday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='w_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End t on Wednesday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='w_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Wednesday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='x_e_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='End time on Sunday'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityruleweekly',
            name='x_s_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Start time on Sunday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruledaily',
            name='ending_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Ending time for the rule'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruledaily',
            name='starting_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Starting time for the rule'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruleonce',
            name='ending_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Ending time for the rule'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availabilityruleonce',
            name='starting_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Starting time for the rule'),
            preserve_default=True,
        ),
    ]
