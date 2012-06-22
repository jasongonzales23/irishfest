# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table('inventory_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('inventory', ['Token'])

        # Adding model 'TokenCollection'
        db.create_table('inventory_tokencollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tokens', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('inventory', ['TokenCollection'])

        # Adding model 'TokenNote'
        db.create_table('inventory_tokennote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Location'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=50000)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('inventory', ['TokenNote'])

        # Adding model 'TokenDelivery'
        db.create_table('inventory_tokendelivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tokens', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('inventory', ['TokenDelivery'])

        # Adding model 'TokenBooth'
        db.create_table('inventory_tokenbooth', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['TokenBooth'])


    def backwards(self, orm):
        # Deleting model 'Token'
        db.delete_table('inventory_token')

        # Deleting model 'TokenCollection'
        db.delete_table('inventory_tokencollection')

        # Deleting model 'TokenNote'
        db.delete_table('inventory_tokennote')

        # Deleting model 'TokenDelivery'
        db.delete_table('inventory_tokendelivery')

        # Deleting model 'TokenBooth'
        db.delete_table('inventory_tokenbooth')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inventory.beverage': {
            'Meta': {'object_name': 'Beverage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tokenvalue': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.InventoryGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'units_reported': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'inventory.inventorygroup': {
            'Meta': {'object_name': 'InventoryGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'inventory.order': {
            'Meta': {'object_name': 'Order'},
            'beverage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Beverage']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.OrderGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'order_delivered': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'units_ordered': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'inventory.ordergroup': {
            'Meta': {'object_name': 'OrderGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'inventory.token': {
            'Meta': {'object_name': 'Token'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'inventory.tokenbooth': {
            'Meta': {'object_name': 'TokenBooth'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.tokencollection': {
            'Meta': {'object_name': 'TokenCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tokens': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'inventory.tokendelivery': {
            'Meta': {'object_name': 'TokenDelivery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tokens': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'inventory.tokennote': {
            'Meta': {'object_name': 'TokenNote'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '50000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Location']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['inventory']