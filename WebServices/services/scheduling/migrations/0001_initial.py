# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OperationalSlot'
        db.create_table(u'scheduling_operationalslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('groundstation_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.GroundStationChannel'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('spacecraft_channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.SpacecraftChannel'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'FREE', max_length=10)),
            ('gs_notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sc_notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('availability_slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['configuration.AvailabilitySlot'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('scheduling', ['OperationalSlot'])


    def backwards(self, orm):
        # Deleting model 'OperationalSlot'
        db.delete_table(u'scheduling_operationalslot')


    models = {
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
        'scheduling.operationalslot': {
            'Meta': {'object_name': 'OperationalSlot'},
            'availability_slot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.AvailabilitySlot']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'groundstation_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.GroundStationChannel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'gs_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'sc_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spacecraft_channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['configuration.SpacecraftChannel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'FREE'", 'max_length': '10'})
        }
    }

    complete_apps = ['scheduling']