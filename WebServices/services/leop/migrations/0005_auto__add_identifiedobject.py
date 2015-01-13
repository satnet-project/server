# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdentifiedObject'
        db.create_table(u'leop_identifiedobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('spacecraft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.Spacecraft'])),
        ))
        db.send_create_signal('leop', ['IdentifiedObject'])


    def backwards(self, orm):
        # Deleting model 'IdentifiedObject'
        db.delete_table(u'leop_identifiedobject')


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
        },
        'leop.identifiedobject': {
            'Meta': {'object_name': 'IdentifiedObject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'spacecraft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.Spacecraft']"})
        },
        'leop.launch': {
            'Meta': {'object_name': 'Launch'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"}),
            'cluster_spacecraft_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'groundstations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['configuration.GroundStation']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identified_objects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['leop.IdentifiedObject']", 'symmetrical': 'False'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'tle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.TwoLineElement']"}),
            'unknown_objects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['leop.UnknownObject']", 'symmetrical': 'False'})
        },
        'leop.unknownobject': {
            'Meta': {'object_name': 'UnknownObject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['leop']