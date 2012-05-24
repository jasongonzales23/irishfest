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

        # Adding M2M table for field beverages on 'Location'
        db.create_table('inventory_location_beverages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['inventory.location'], null=False)),
            ('beverage', models.ForeignKey(orm['inventory.beverage'], null=False))
        ))
        db.create_unique('inventory_location_beverages', ['location_id', 'beverage_id'])

        # Adding model 'LocationStandard'
        db.create_table('inventory_locationstandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beverage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Beverage'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('fill_to_standard', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('order_when_below', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('inventory', ['LocationStandard'])


    def backwards(self, orm):
        # Deleting model 'Beverage'
        db.delete_table('inventory_beverage')

        # Deleting model 'Location'
        db.delete_table('inventory_location')

        # Removing M2M table for field beverages on 'Location'
        db.delete_table('inventory_location_beverages')

        # Deleting model 'LocationStandard'
        db.delete_table('inventory_locationstandard')


    models = {
        'inventory.beverage': {
            'Meta': {'object_name': 'Beverage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        }
    }

    complete_apps = ['inventory']