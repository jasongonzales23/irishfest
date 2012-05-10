# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Locations'
        db.create_table('inventory_locations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['Locations'])

        # Adding model 'Beverages'
        db.create_table('inventory_beverages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('units_reported', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('fill_to_standard', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('order_when_below', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('inventory', ['Beverages'])

        # Adding model 'Orders'
        db.create_table('inventory_orders', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Orders'])

        # Adding model 'Inventory'
        db.create_table('inventory_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Locations'])),
            ('beverage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Beverages'])),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=2550)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Inventory'])


    def backwards(self, orm):
        # Deleting model 'Locations'
        db.delete_table('inventory_locations')

        # Deleting model 'Beverages'
        db.delete_table('inventory_beverages')

        # Deleting model 'Orders'
        db.delete_table('inventory_orders')

        # Deleting model 'Inventory'
        db.delete_table('inventory_inventory')


    models = {
        'inventory.beverages': {
            'Meta': {'object_name': 'Beverages'},
            'fill_to_standard': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_when_below': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'units_reported': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverages']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Locations']"}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '2550'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'inventory.locations': {
            'Meta': {'object_name': 'Locations'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.orders': {
            'Meta': {'object_name': 'Orders'},
            'amount': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']