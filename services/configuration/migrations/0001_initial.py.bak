# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilityRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation', models.CharField(max_length=1, verbose_name=b'Operation that this rule defines', choices=[(b'+', b'Operation for adding new slots'), (b'-', b'Operation for removing existing slots')])),
                ('periodicity', models.CharField(max_length=1, verbose_name=b'Period of time that this rule occurs.', choices=[(b'O', b'Rule that occurs only once.'), (b'D', b'Rule that defines daily repetition pattern.'), (b'W', b'Rule that defines a weekly repetition pattern.')])),
                ('starting_date', models.DateField(verbose_name=b'Starting date for an availability period')),
                ('ending_date', models.DateField(verbose_name=b'Ending date for an availability period')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleDaily',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='configuration.AvailabilityRule')),
                ('starting_time', models.TimeField(verbose_name=b'Starting time for a daily period.')),
                ('ending_time', models.TimeField(verbose_name=b'Ending time for a daily period.')),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleOnce',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='configuration.AvailabilityRule')),
                ('starting_time', models.TimeField(verbose_name=b'Beginning date and time for the rule.')),
                ('ending_time', models.TimeField(verbose_name=b'Ending date and time for the rule.')),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailabilityRuleWeekly',
            fields=[
                ('availabilityrule_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='configuration.AvailabilityRule')),
                ('monday_starting_time', models.TimeField(verbose_name=b'Starting time on Monday.')),
                ('monday_ending_time', models.TimeField(verbose_name=b'Ending time on this Monday.')),
                ('tuesday_starting_time', models.TimeField(verbose_name=b'Starting time on Tuesday.')),
                ('tuesday_ending_time', models.TimeField(verbose_name=b'Ending time on this Tuesday.')),
                ('wednesday_starting_time', models.TimeField(verbose_name=b'Starting time on Wednesday.')),
                ('wednesday_ending_time', models.TimeField(verbose_name=b'Ending time on this Wednesday.')),
                ('thursday_starting_time', models.TimeField(verbose_name=b'Starting time on Thursday.')),
                ('thursday_ending_time', models.TimeField(verbose_name=b'Ending time on this Thursday.')),
                ('friday_starting_time', models.TimeField(verbose_name=b'Starting time on Friday.')),
                ('friday_ending_time', models.TimeField(verbose_name=b'Ending time on this Friday.')),
                ('saturday_starting_time', models.TimeField(verbose_name=b'Starting time on Saturday.')),
                ('saturday_ending_time', models.TimeField(verbose_name=b'Ending time on this Saturday.')),
                ('sunday_starting_time', models.TimeField(verbose_name=b'Starting time on Sunday.')),
                ('sunday_ending_time', models.TimeField(verbose_name=b'Ending time on this Sunday.')),
            ],
            options={
            },
            bases=('configuration.availabilityrule',),
        ),
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=100, verbose_name=b'Unique identifier for this slot')),
                ('start', models.DateTimeField(verbose_name=b'Slot start')),
                ('end', models.DateTimeField(verbose_name=b'Slot end')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableBands',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('IARU_range', models.CharField(max_length=4, verbose_name=b'IARU Range')),
                ('IARU_band', models.CharField(max_length=6, verbose_name=b'IARU Band')),
                ('AMSAT_letter', models.CharField(max_length=4, verbose_name=b'AMSAT Letter')),
                ('IARU_allocation_minimum_frequency', models.DecimalField(verbose_name=b'Minimum frequency (MHz)', max_digits=24, decimal_places=6)),
                ('IARU_allocation_maximum_frequency', models.DecimalField(verbose_name=b'Maximum frequency (MHz)', max_digits=24, decimal_places=6)),
                ('uplink', models.BooleanField(default=False, verbose_name=b'Uplink permitted')),
                ('downlink', models.BooleanField(default=False, verbose_name=b'Downlink permitted')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableBandwidths',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bandwidth', models.DecimalField(verbose_name=b'Bandwidth (kHz)', max_digits=24, decimal_places=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableBitrates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bitrate', models.IntegerField(verbose_name=b'Bitrate (bps)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailableModulations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modulation', models.CharField(max_length=9, verbose_name=b'Modulation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AvailablePolarizations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polarization', models.CharField(max_length=10, verbose_name=b'Polarization modes', choices=[(b'Any', b'Any polarization type'), (b'RHCP', b'RHCP polarization'), (b'LHCP', b'LHCP polarization')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChannelCompatibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroundStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'Unique alphanumeric identifier for this GroundStation', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_spacecraft_identifier')])),
                ('callsign', models.CharField(max_length=10, verbose_name=b'Radio amateur callsign for this GroundStation', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_callsign')])),
                ('contact_elevation', models.FloatField(verbose_name=b'Minimum elevation for contact(degrees)')),
                ('latitude', models.FloatField(verbose_name=b'Latitude of the Ground Station')),
                ('longitude', models.FloatField(verbose_name=b'Longitude of the Ground Station')),
                ('altitude', models.FloatField(verbose_name=b'Altitude of the Ground Station')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name=b'Country where the GroundStation is located')),
                ('IARU_region', models.SmallIntegerField(verbose_name=b'IARU region identifier')),
                ('is_automatic', models.BooleanField(default=False, verbose_name=b'Flag that defines this GroundStation as a fully automated one,so that it will automatically accept any operation request from a remote Spacecraft operator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroundStationChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True, verbose_name=b'Enables the usage of this channel')),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'Unique identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_channel_identifier')])),
                ('automated', models.BooleanField(default=False, verbose_name=b'Defines this channel as fully automated')),
                ('band', models.ForeignKey(to='configuration.AvailableBands')),
                ('bandwidths', models.ManyToManyField(to='configuration.AvailableBandwidths')),
                ('bitrates', models.ManyToManyField(to='configuration.AvailableBitrates')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'Identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_spacecraft_identifier')])),
                ('callsign', models.CharField(max_length=10, verbose_name=b'Radio amateur callsign', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_callsign')])),
                ('is_cluster', models.BooleanField(default=False, verbose_name=b'Flag that indicates whether this object is a cluster or not')),
                ('is_ufo', models.BooleanField(default=False, verbose_name=b'Flag that defines whether this object is an UFO or not')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpacecraftChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True, verbose_name=b'Enables the usage of this channel')),
                ('identifier', models.CharField(unique=True, max_length=30, verbose_name=b'Unique identifier', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.-_]*$', message=b"Alphanumeric or '.-_' required", code=b'invalid_channel_identifier')])),
                ('frequency', models.DecimalField(verbose_name=b'Central frequency (Hz)', max_digits=15, decimal_places=3)),
                ('bandwidth', models.ForeignKey(to='configuration.AvailableBandwidths')),
                ('bitrate', models.ForeignKey(to='configuration.AvailableBitrates')),
                ('modulation', models.ForeignKey(to='configuration.AvailableModulations')),
                ('polarization', models.ForeignKey(to='configuration.AvailablePolarizations')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwoLineElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=24, verbose_name=b'Identifier of the spacecraft that this TLE element models (line 0)')),
                ('timestamp', models.BigIntegerField(verbose_name=b'Timestamp with the update date for this TLE')),
                ('source', models.TextField(max_length=100, verbose_name=b'String that indicates the source of this TLE', validators=[django.core.validators.URLValidator()])),
                ('first_line', models.CharField(max_length=69, verbose_name=b'First line of this TLE', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\s-]{69}$', message=b"Alphanumeric or '.-_' required", code=b'invalid_tle_line_1')])),
                ('second_line', models.CharField(max_length=69, verbose_name=b'Second line of this TLE', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9.\\s-]{69}$', message=b"Alphanumeric or '.-_' required", code=b'invalid_tle_line_2')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='spacecraft',
            name='channels',
            field=models.ManyToManyField(to='configuration.SpacecraftChannel', verbose_name=b'Available spacecraft communications channels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spacecraft',
            name='tle',
            field=models.ForeignKey(verbose_name=b'TLE object for this Spacecraft', to='configuration.TwoLineElement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spacecraft',
            name='user',
            field=models.ForeignKey(verbose_name=b'Owner of the Spacecraft', to='accounts.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groundstation',
            name='channels',
            field=models.ManyToManyField(to='configuration.GroundStationChannel', verbose_name=b'Communication channels that belong to this GroundStation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groundstation',
            name='user',
            field=models.ForeignKey(verbose_name=b'User to which this GroundStation belongs to', to='accounts.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channelcompatibility',
            name='groundstation_channels',
            field=models.ManyToManyField(to='configuration.GroundStationChannel', verbose_name=b'Reference to all the compatible GroundStation channels.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channelcompatibility',
            name='spacecraft_channel',
            field=models.ForeignKey(verbose_name=b'Reference to the compatible Spacecraft channel.', to='configuration.SpacecraftChannel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityslot',
            name='groundstation_channel',
            field=models.ForeignKey(verbose_name=b'GroundStationChannel that this slot belongs to', to='configuration.GroundStationChannel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availabilityrule',
            name='gs_channel',
            field=models.ForeignKey(verbose_name=b'Channel that this rule belongs to.', to='configuration.GroundStationChannel'),
            preserve_default=True,
        ),
    ]
