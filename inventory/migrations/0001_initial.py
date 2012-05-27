# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Beverage'
        db.create_table('inventory_beverage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['Beverage'])

        # Adding model 'Location'
        db.create_table('inventory_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['Location'])

        # Adding model 'LocationStandard'
        db.create_table('inventory_locationstandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beverage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Beverage'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('start_units', self.gf('django.db.models.fields.IntegerField')()),
            ('fill_to_standard', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('order_when_below', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('inventory', ['LocationStandard'])

        # Adding model 'Order'
        db.create_table('inventory_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('beverage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Beverage'])),
            ('units_ordered', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('order_delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Order'])

        # Adding model 'Inventory'
        db.create_table('inventory_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('beverage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Beverage'])),
            ('units_reported', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Inventory'])

        # Adding model 'Note'
        db.create_table('inventory_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=50000)),
        ))
        db.send_create_signal('inventory', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Beverage'
        db.delete_table('inventory_beverage')

        # Deleting model 'Location'
        db.delete_table('inventory_location')

        # Deleting model 'LocationStandard'
        db.delete_table('inventory_locationstandard')

        # Deleting model 'Order'
        db.delete_table('inventory_order')

        # Deleting model 'Inventory'
        db.delete_table('inventory_inventory')

        # Deleting model 'Note'
        db.delete_table('inventory_note')


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
            'beverages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Beverage']", 'through': "orm['inventory.LocationStandard']", 'symmetrical': 'False'}),
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
            'order_when_below': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'start_units': ('django.db.models.fields.IntegerField', [], {})
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
        }
    }

    complete_apps = ['inventory']