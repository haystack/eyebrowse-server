# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table('tags_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
        ))
        db.send_create_signal('tags', ['Domain'])

        # Adding model 'Page'
        db.create_table('tags_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Domain'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=2000)),
            ('favicon_url', self.gf('django.db.models.fields.TextField')(default='')),
            ('favIconUrl', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('img_url', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
        ))
        db.send_create_signal('tags', ['Page'])

        # Adding model 'Highlight'
        db.create_table('tags_highlight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('highlight', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Page'])),
        ))
        db.send_create_signal('tags', ['Highlight'])


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table('tags_domain')

        # Deleting model 'Page'
        db.delete_table('tags_page')

        # Deleting model 'Highlight'
        db.delete_table('tags_highlight')


    models = {
        'tags.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        'tags.highlight': {
            'Meta': {'object_name': 'Highlight'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Page']"})
        },
        'tags.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Domain']"}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['tags']