# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Page.favicon_url'
        db.delete_column('tags_page', 'favicon_url')

        # Deleting field 'Page.description'
        db.delete_column('tags_page', 'description')

        # Deleting field 'Page.title'
        db.delete_column('tags_page', 'title')

        # Deleting field 'Page.favIconUrl'
        db.delete_column('tags_page', 'favIconUrl')

        # Deleting field 'Page.img_url'
        db.delete_column('tags_page', 'img_url')


    def backwards(self, orm):
        # Adding field 'Page.favicon_url'
        db.add_column('tags_page', 'favicon_url',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Page.description'
        db.add_column('tags_page', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Page.title'
        db.add_column('tags_page', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2000),
                      keep_default=False)

        # Adding field 'Page.favIconUrl'
        db.add_column('tags_page', 'favIconUrl',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=2000),
                      keep_default=False)

        # Adding field 'Page.img_url'
        db.add_column('tags_page', 'img_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=2000),
                      keep_default=False)


    models = {
        'tags.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '100'}),
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
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['tags']