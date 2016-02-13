# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilityRule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('operation', models.CharField(verbose_name='Rule operation', max_length=1, choices=[('+', 'Operation for adding new slots'), ('-', 'Operation for removing existing slots')])),
                ('periodicity', models.CharField(verbose_name='Rule periodicity', max_length=1, choices=[('O', 'Rule that occurs only once.'), ('D', 'Rule that defines daily repetition pattern.'), ('W', 'Rule that defines a weekly repetition pattern.')])),
                ('starting_date', models.DateField(null=True, verbose_name='Starting date for the applicability period of the rule', default=django.utils.timezone.now)),
                ('ending_date', models.DateField(null=True, verbose_name='Ending date for the applicability period of the rule', default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleDaily',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='configuration.AvailabilityRule', serialize=False)),
                ('starting_time', models.DateTimeField(null=True, verbose_name='Starting time for the rule', default=django.utils.timezone.now)),
                ('ending_time', models.DateTimeField(null=True, verbose_name='Ending time for the rule', default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleOnce',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='configuration.AvailabilityRule', serialize=False)),
                ('starting_time', models.DateTimeField(null=True, verbose_name='Starting datetime for the rule', default=django.utils.timezone.now)),
                ('ending_time', models.DateTimeField(null=True, verbose_name='Ending datetime for the rule', default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleWeekly',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='configuration.AvailabilityRule', serialize=False)),
                ('m_s_time', models.DateTimeField(null=True, verbose_name='Start time on Monday', default=django.utils.timezone.now)),
                ('m_e_time', models.DateTimeField(null=True, verbose_name='End time on Monday', default=django.utils.timezone.now)),
                ('t_s_time', models.DateTimeField(null=True, verbose_name='Start time on Tuesday', default=django.utils.timezone.now)),
                ('t_e_time', models.DateTimeField(null=True, verbose_name='End time on Tuesday', default=django.utils.timezone.now)),
                ('w_s_time', models.DateTimeField(null=True, verbose_name='Start time on Wednesday', default=django.utils.timezone.now)),
                ('w_e_time', models.DateTimeField(null=True, verbose_name='End t on Wednesday', default=django.utils.timezone.now)),
                ('r_s_time', models.DateTimeField(null=True, verbose_name='Start time on Thursday', default=django.utils.timezone.now)),
                ('r_e_time', models.DateTimeField(null=True, verbose_name='End time on Thursday', default=django.utils.timezone.now)),
                ('f_s_time', models.DateTimeField(null=True, verbose_name='Start time on Friday', default=django.utils.timezone.now)),
                ('f_e_time', models.DateTimeField(null=True, verbose_name='End time on Friday', default=django.utils.timezone.now)),
                ('s_s_time', models.DateTimeField(null=True, verbose_name='Start time on Saturday', default=django.utils.timezone.now)),
                ('s_e_time', models.DateTimeField(null=True, verbose_name='End time on Saturday', default=django.utils.timezone.now)),
                ('x_s_time', models.DateTimeField(null=True, verbose_name='Start time on Sunday', default=django.utils.timezone.now)),
                ('x_e_time', models.DateTimeField(null=True, verbose_name='End time on Sunday', default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailableBands',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('IARU_range', models.CharField(verbose_name='IARU Range', max_length=4)),
                ('IARU_band', models.CharField(verbose_name='IARU Band', max_length=6)),
                ('AMSAT_letter', models.CharField(verbose_name='AMSAT Letter', max_length=4)),
                ('IARU_allocation_minimum_frequency', models.DecimalField(verbose_name='Minimum frequency (MHz)', decimal_places=6, max_digits=24)),
                ('IARU_allocation_maximum_frequency', models.DecimalField(verbose_name='Maximum frequency (MHz)', decimal_places=6, max_digits=24)),
                ('uplink', models.BooleanField(verbose_name='Uplink permitted', default=False)),
                ('downlink', models.BooleanField(verbose_name='Downlink permitted', default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableBandwidths',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('bandwidth', models.DecimalField(verbose_name='Bandwidth (kHz)', decimal_places=9, max_digits=24)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableBitrates',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('bitrate', models.IntegerField(verbose_name='Bitrate (bps)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableModulations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('modulation', models.CharField(verbose_name='Modulation', max_length=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailablePolarizations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('polarization', models.CharField(verbose_name='Polarization modes', max_length=10, choices=[('Any', 'Any polarization type'), ('RHCP', 'RHCP polarization'), ('LHCP', 'LHCP polarization')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroundStation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name='Unique alphanumeric identifier for this GroundStation', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_spacecraft_identifier')])),
                ('callsign', models.CharField(verbose_name='Radio amateur callsign for this GroundStation', max_length=10, validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_callsign')])),
                ('contact_elevation', models.FloatField(verbose_name='Minimum elevation for contact(degrees)')),
                ('latitude', models.FloatField(verbose_name='Latitude of the Ground Station')),
                ('longitude', models.FloatField(verbose_name='Longitude of the Ground Station')),
                ('altitude', models.FloatField(verbose_name='Altitude of the Ground Station')),
                ('country', django_countries.fields.CountryField(verbose_name='Country where the GroundStation is located', max_length=2)),
                ('IARU_region', models.SmallIntegerField(verbose_name='IARU region identifier')),
                ('is_automatic', models.BooleanField(verbose_name='Flag that defines this GroundStation as a fully automated one,so that it will automatically accept any operation request from a remote Spacecraft operator', default=False)),
                ('user', models.ForeignKey(verbose_name='User to which this GroundStation belongs to', to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroundStationChannel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('enabled', models.BooleanField(verbose_name='Enables the usage of this channel', default=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name='Unique identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.-_]*$', code='invalid_channel_identifier')])),
                ('automated', models.BooleanField(verbose_name='Defines this channel as fully automated', default=False)),
                ('band', models.ForeignKey(verbose_name='Band for the channel of the Ground Station', to='configuration.AvailableBands')),
                ('bandwidths', models.ManyToManyField(to='configuration.AvailableBandwidths')),
                ('bitrates', models.ManyToManyField(to='configuration.AvailableBitrates')),
                ('groundstation', models.ForeignKey(verbose_name='Ground Station that this channel belongs to', default=1, to='configuration.GroundStation')),
                ('modulations', models.ManyToManyField(to='configuration.AvailableModulations')),
                ('polarizations', models.ManyToManyField(to='configuration.AvailablePolarizations')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spacecraft',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name='Identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_spacecraft_identifier')])),
                ('callsign', models.CharField(verbose_name='Radio amateur callsign', max_length=10, validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\-_]*$', code='invalid_callsign')])),
                ('is_cluster', models.BooleanField(verbose_name='Flag that indicates whether this object is a cluster or not', default=False)),
                ('is_ufo', models.BooleanField(verbose_name='Flag that defines whether this object is an UFO or not', default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpacecraftChannel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('enabled', models.BooleanField(verbose_name='Enables the usage of this channel', default=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name='Unique identifier', validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.-_]*$', code='invalid_channel_identifier')])),
                ('frequency', models.DecimalField(verbose_name='Central frequency (Hz)', decimal_places=3, max_digits=15)),
                ('bandwidth', models.ForeignKey(to='configuration.AvailableBandwidths')),
                ('bitrate', models.ForeignKey(to='configuration.AvailableBitrates')),
                ('modulation', models.ForeignKey(to='configuration.AvailableModulations')),
                ('polarization', models.ForeignKey(to='configuration.AvailablePolarizations')),
                ('spacecraft', models.ForeignKey(verbose_name='Spacecraft that this channel belongs to', default=1, to='configuration.Spacecraft')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwoLineElement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', models.CharField(unique=True, max_length=24, verbose_name='Identifier of the spacecraft that this TLE element models (line 0)')),
                ('timestamp', models.BigIntegerField(verbose_name='Timestamp with the update date for this TLE')),
                ('source', models.TextField(verbose_name='String that indicates the source of this TLE', max_length=100, validators=[django.core.validators.URLValidator()])),
                ('first_line', models.CharField(verbose_name='First line of this TLE', max_length=69, validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\s-]{69}$', code='invalid_tle_line_1')])),
                ('second_line', models.CharField(verbose_name='Second line of this TLE', max_length=69, validators=[django.core.validators.RegexValidator(message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\s-]{69}$', code='invalid_tle_line_2')])),
            ],
            options={
                'ordering': ['identifier'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spacecraft',
            name='tle',
            field=models.ForeignKey(verbose_name='TLE object for this Spacecraft', to='configuration.TwoLineElement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spacecraft',
            name='user',
            field=models.ForeignKey(verbose_name='Owner of the Spacecraft', to='accounts.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityrule',
            name='groundstation',
            field=models.ForeignKey(verbose_name='Reference to the Ground Station that owns this rule', default=1, to='configuration.GroundStation'),
            preserve_default=True,
        ),
    ]
