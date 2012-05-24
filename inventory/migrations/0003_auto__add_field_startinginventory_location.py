# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StartingInventory.location'
        db.add_column('inventory_startinginventory', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['inventory.Location']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StartingInventory.location'
        db.delete_column('inventory_startinginventory', 'location_id')


    models = {
        'inventory.beverage': {
            'Meta': {'object_name': 'Beverage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'units_reported': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'})
        },
        'inventory.location': {
            'Meta': {'object_name': 'Location'},
            'beverages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'locations'", 'symmetrical': 'False', 'to': "orm['inventory.Beverage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.locationstandard': {
            'Meta': {'object_name': 'LocationStandard'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'fill_to_standard': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'order_when_below': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        'inventory.note': {
            'Meta': {'object_name': 'Note'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '50000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'inventory.order': {
            'Meta': {'object_name': 'Order'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'order_delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'units_ordered': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'})
        },
        'inventory.startinginventory': {
            'Meta': {'object_name': 'StartingInventory'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['inventory']