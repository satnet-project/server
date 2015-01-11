# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AvailableModulations'
        db.create_table(u'configuration_availablemodulations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modulation', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('configuration', ['AvailableModulations'])

        # Adding model 'AvailableBitrates'
        db.create_table(u'configuration_availablebitrates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bitrate', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('configuration', ['AvailableBitrates'])

        # Adding model 'AvailableBandwidths'
        db.create_table(u'configuration_availablebandwidths', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bandwidth', self.gf('django.db.models.fields.DecimalField')(max_digits=24, decimal_places=9)),
        ))
        db.send_create_signal('configuration', ['AvailableBandwidths'])

        # Adding model 'AvailablePolarizations'
        db.create_table(u'configuration_availablepolarizations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polarization', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('configuration', ['AvailablePolarizations'])

        # Adding model 'AvailableBands'
        db.create_table(u'configuration_availablebands', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('IARU_range', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('IARU_band', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('AMSAT_letter', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('IARU_allocation_minimum_frequency', self.gf('django.db.models.fields.DecimalField')(max_digits=24, decimal_places=6)),
            ('IARU_allocation_maximum_frequency', self.gf('django.db.models.fields.DecimalField')(max_digits=24, decimal_places=6)),
            ('uplink', self.gf('django.db.models.fields.BooleanField')()),
            ('downlink', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('configuration', ['AvailableBands'])

        # Adding model 'SpacecraftChannel'
        db.create_table(u'configuration_spacecraftchannel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('modulation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailableModulations'])),
            ('bitrate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailableBitrates'])),
            ('bandwidth', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailableBandwidths'])),
            ('polarization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailablePolarizations'])),
            ('frequency', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=3)),
        ))
        db.send_create_signal('configuration', ['SpacecraftChannel'])

        # Adding model 'GroundStationChannel'
        db.create_table(u'configuration_groundstationchannel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('automated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailableBands'])),
        ))
        db.send_create_signal('configuration', ['GroundStationChannel'])

        # Adding M2M table for field modulations on 'GroundStationChannel'
        m2m_table_name = db.shorten_name(u'configuration_groundstationchannel_modulations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False)),
            ('availablemodulations', models.ForeignKey(orm['configuration.availablemodulations'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groundstationchannel_id', 'availablemodulations_id'])

        # Adding M2M table for field bitrates on 'GroundStationChannel'
        m2m_table_name = db.shorten_name(u'configuration_groundstationchannel_bitrates')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False)),
            ('availablebitrates', models.ForeignKey(orm['configuration.availablebitrates'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groundstationchannel_id', 'availablebitrates_id'])

        # Adding M2M table for field bandwidths on 'GroundStationChannel'
        m2m_table_name = db.shorten_name(u'configuration_groundstationchannel_bandwidths')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False)),
            ('availablebandwidths', models.ForeignKey(orm['configuration.availablebandwidths'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groundstationchannel_id', 'availablebandwidths_id'])

        # Adding M2M table for field polarizations on 'GroundStationChannel'
        m2m_table_name = db.shorten_name(u'configuration_groundstationchannel_polarizations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False)),
            ('availablepolarizations', models.ForeignKey(orm['configuration.availablepolarizations'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groundstationchannel_id', 'availablepolarizations_id'])

        # Adding model 'TwoLineElement'
        db.create_table(u'configuration_twolineelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('timestamp', self.gf('django.db.models.fields.BigIntegerField')()),
            ('source', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('first_line', self.gf('django.db.models.fields.CharField')(max_length=69)),
            ('second_line', self.gf('django.db.models.fields.CharField')(max_length=69)),
        ))
        db.send_create_signal('configuration', ['TwoLineElement'])

        # Adding model 'Spacecraft'
        db.create_table(u'configuration_spacecraft', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('callsign', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.TwoLineElement'])),
            ('is_cluster', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_ufo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('configuration', ['Spacecraft'])

        # Adding M2M table for field channels on 'Spacecraft'
        m2m_table_name = db.shorten_name(u'configuration_spacecraft_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spacecraft', models.ForeignKey(orm['configuration.spacecraft'], null=False)),
            ('spacecraftchannel', models.ForeignKey(orm['configuration.spacecraftchannel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['spacecraft_id', 'spacecraftchannel_id'])

        # Adding model 'GroundStation'
        db.create_table(u'configuration_groundstation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('callsign', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('contact_elevation', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('IARU_region', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('is_automatic', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('configuration', ['GroundStation'])

        # Adding M2M table for field channels on 'GroundStation'
        m2m_table_name = db.shorten_name(u'configuration_groundstation_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groundstation', models.ForeignKey(orm['configuration.groundstation'], null=False)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groundstation_id', 'groundstationchannel_id'])

        # Adding model 'AvailabilityRule'
        db.create_table(u'configuration_availabilityrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gs_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.GroundStationChannel'])),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('periodicity', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('starting_date', self.gf('django.db.models.fields.DateField')()),
            ('ending_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('configuration', ['AvailabilityRule'])

        # Adding model 'AvailabilityRuleOnce'
        db.create_table(u'configuration_availabilityruleonce', (
            (u'availabilityrule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['configuration.AvailabilityRule'], unique=True, primary_key=True)),
            ('starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('ending_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('configuration', ['AvailabilityRuleOnce'])

        # Adding model 'AvailabilityRuleDaily'
        db.create_table(u'configuration_availabilityruledaily', (
            (u'availabilityrule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['configuration.AvailabilityRule'], unique=True, primary_key=True)),
            ('starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('ending_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('configuration', ['AvailabilityRuleDaily'])

        # Adding model 'AvailabilityRuleWeekly'
        db.create_table(u'configuration_availabilityruleweekly', (
            (u'availabilityrule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['configuration.AvailabilityRule'], unique=True, primary_key=True)),
            ('monday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('monday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('tuesday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('tuesday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('wednesday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('wednesday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('thursday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('thursday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('friday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('friday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('saturday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('saturday_ending_time', self.gf('django.db.models.fields.TimeField')()),
            ('sunday_starting_time', self.gf('django.db.models.fields.TimeField')()),
            ('sunday_ending_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('configuration', ['AvailabilityRuleWeekly'])

        # Adding model 'AvailabilitySlot'
        db.create_table(u'configuration_availabilityslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('groundstation_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.GroundStationChannel'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('configuration', ['AvailabilitySlot'])

        # Adding model 'ChannelCompatibility'
        db.create_table(u'configuration_channelcompatibility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spacecraft_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.SpacecraftChannel'])),
        ))
        db.send_create_signal('configuration', ['ChannelCompatibility'])

        # Adding M2M table for field groundstation_channels on 'ChannelCompatibility'
        m2m_table_name = db.shorten_name(u'configuration_channelcompatibility_groundstation_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channelcompatibility', models.ForeignKey(orm['configuration.channelcompatibility'], null=False)),
            ('groundstationchannel', models.ForeignKey(orm['configuration.groundstationchannel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['channelcompatibility_id', 'groundstationchannel_id'])


    def backwards(self, orm):
        # Deleting model 'AvailableModulations'
        db.delete_table(u'configuration_availablemodulations')

        # Deleting model 'AvailableBitrates'
        db.delete_table(u'configuration_availablebitrates')

        # Deleting model 'AvailableBandwidths'
        db.delete_table(u'configuration_availablebandwidths')

        # Deleting model 'AvailablePolarizations'
        db.delete_table(u'configuration_availablepolarizations')

        # Deleting model 'AvailableBands'
        db.delete_table(u'configuration_availablebands')

        # Deleting model 'SpacecraftChannel'
        db.delete_table(u'configuration_spacecraftchannel')

        # Deleting model 'GroundStationChannel'
        db.delete_table(u'configuration_groundstationchannel')

        # Removing M2M table for field modulations on 'GroundStationChannel'
        db.delete_table(db.shorten_name(u'configuration_groundstationchannel_modulations'))

        # Removing M2M table for field bitrates on 'GroundStationChannel'
        db.delete_table(db.shorten_name(u'configuration_groundstationchannel_bitrates'))

        # Removing M2M table for field bandwidths on 'GroundStationChannel'
        db.delete_table(db.shorten_name(u'configuration_groundstationchannel_bandwidths'))

        # Removing M2M table for field polarizations on 'GroundStationChannel'
        db.delete_table(db.shorten_name(u'configuration_groundstationchannel_polarizations'))

        # Deleting model 'TwoLineElement'
        db.delete_table(u'configuration_twolineelement')

        # Deleting model 'Spacecraft'
        db.delete_table(u'configuration_spacecraft')

        # Removing M2M table for field channels on 'Spacecraft'
        db.delete_table(db.shorten_name(u'configuration_spacecraft_channels'))

        # Deleting model 'GroundStation'
        db.delete_table(u'configuration_groundstation')

        # Removing M2M table for field channels on 'GroundStation'
        db.delete_table(db.shorten_name(u'configuration_groundstation_channels'))

        # Deleting model 'AvailabilityRule'
        db.delete_table(u'configuration_availabilityrule')

        # Deleting model 'AvailabilityRuleOnce'
        db.delete_table(u'configuration_availabilityruleonce')

        # Deleting model 'AvailabilityRuleDaily'
        db.delete_table(u'configuration_availabilityruledaily')

        # Deleting model 'AvailabilityRuleWeekly'
        db.delete_table(u'configuration_availabilityruleweekly')

        # Deleting model 'AvailabilitySlot'
        db.delete_table(u'configuration_availabilityslot')

        # Deleting model 'ChannelCompatibility'
        db.delete_table(u'configuration_channelcompatibility')

        # Removing M2M table for field groundstation_channels on 'ChannelCompatibility'
        db.delete_table(db.shorten_name(u'configuration_channelcompatibility_groundstation_channels'))


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': [u'auth.User']},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'configuration.availabilityrule': {
            'Meta': {'object_name': 'AvailabilityRule'},
            'ending_date': ('django.db.models.fields.DateField', [], {}),
            'gs_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.GroundStationChannel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'periodicity': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'starting_date': ('django.db.models.fields.DateField', [], {})
        },
        'configuration.availabilityruledaily': {
            'Meta': {'object_name': 'AvailabilityRuleDaily', '_ormbases': ['configuration.AvailabilityRule']},
            u'availabilityrule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['configuration.AvailabilityRule']", 'unique': 'True', 'primary_key': 'True'}),
            'ending_time': ('django.db.models.fields.TimeField', [], {}),
            'starting_time': ('django.db.models.fields.TimeField', [], {})
        },
        'configuration.availabilityruleonce': {
            'Meta': {'object_name': 'AvailabilityRuleOnce', '_ormbases': ['configuration.AvailabilityRule']},
            u'availabilityrule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['configuration.AvailabilityRule']", 'unique': 'True', 'primary_key': 'True'}),
            'ending_time': ('django.db.models.fields.TimeField', [], {}),
            'starting_time': ('django.db.models.fields.TimeField', [], {})
        },
        'configuration.availabilityruleweekly': {
            'Meta': {'object_name': 'AvailabilityRuleWeekly', '_ormbases': ['configuration.AvailabilityRule']},
            u'availabilityrule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['configuration.AvailabilityRule']", 'unique': 'True', 'primary_key': 'True'}),
            'friday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'friday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'monday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'monday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'saturday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'saturday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'sunday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'sunday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'thursday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'thursday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'tuesday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'tuesday_starting_time': ('django.db.models.fields.TimeField', [], {}),
            'wednesday_ending_time': ('django.db.models.fields.TimeField', [], {}),
            'wednesday_starting_time': ('django.db.models.fields.TimeField', [], {})
        },
        'configuration.availabilityslot': {
            'Meta': {'object_name': 'AvailabilitySlot'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'groundstation_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.GroundStationChannel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'configuration.availablebands': {
            'AMSAT_letter': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'IARU_allocation_maximum_frequency': ('django.db.models.fields.DecimalField', [], {'max_digits': '24', 'decimal_places': '6'}),
            'IARU_allocation_minimum_frequency': ('django.db.models.fields.DecimalField', [], {'max_digits': '24', 'decimal_places': '6'}),
            'IARU_band': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'IARU_range': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'Meta': {'object_name': 'AvailableBands'},
            'downlink': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uplink': ('django.db.models.fields.BooleanField', [], {})
        },
        'configuration.availablebandwidths': {
            'Meta': {'object_name': 'AvailableBandwidths'},
            'bandwidth': ('django.db.models.fields.DecimalField', [], {'max_digits': '24', 'decimal_places': '9'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'configuration.availablebitrates': {
            'Meta': {'object_name': 'AvailableBitrates'},
            'bitrate': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'configuration.availablemodulations': {
            'Meta': {'object_name': 'AvailableModulations'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulation': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'configuration.availablepolarizations': {
            'Meta': {'object_name': 'AvailablePolarizations'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'configuration.channelcompatibility': {
            'Meta': {'object_name': 'ChannelCompatibility'},
            'groundstation_channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.GroundStationChannel']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spacecraft_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.SpacecraftChannel']"})
        },
        'configuration.groundstation': {
            'IARU_region': ('django.db.models.fields.SmallIntegerField', [], {}),
            'Meta': {'object_name': 'GroundStation'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.GroundStationChannel']", 'symmetrical': 'False'}),
            'contact_elevation': ('django.db.models.fields.FloatField', [], {}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'is_automatic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"})
        },
        'configuration.groundstationchannel': {
            'Meta': {'object_name': 'GroundStationChannel'},
            'automated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailableBands']"}),
            'bandwidths': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.AvailableBandwidths']", 'symmetrical': 'False'}),
            'bitrates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.AvailableBitrates']", 'symmetrical': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'modulations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.AvailableModulations']", 'symmetrical': 'False'}),
            'polarizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.AvailablePolarizations']", 'symmetrical': 'False'})
        },
        'configuration.spacecraft': {
            'Meta': {'object_name': 'Spacecraft'},
            'callsign': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.SpacecraftChannel']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'is_cluster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_ufo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.TwoLineElement']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"})
        },
        'configuration.spacecraftchannel': {
            'Meta': {'object_name': 'SpacecraftChannel'},
            'bandwidth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailableBandwidths']"}),
            'bitrate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailableBitrates']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {}),
            'frequency': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'modulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailableModulations']"}),
            'polarization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailablePolarizations']"})
        },
        'configuration.twolineelement': {
            'Meta': {'object_name': 'TwoLineElement'},
            'first_line': ('django.db.models.fields.CharField', [], {'max_length': '69'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'second_line': ('django.db.models.fields.CharField', [], {'max_length': '69'}),
            'source': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['configuration']