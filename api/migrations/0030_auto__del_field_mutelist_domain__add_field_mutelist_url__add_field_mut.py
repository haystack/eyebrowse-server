# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MuteList', fields ['user', 'domain']
        db.delete_unique('api_mutelist', ['user_id', 'domain'])

        # Deleting field 'MuteList.domain'
        db.delete_column('api_mutelist', 'domain')

        # Adding field 'MuteList.url'
        db.add_column('api_mutelist', 'url',
                      self.gf('django.db.models.fields.URLField')(max_length=300, null=True),
                      keep_default=False)

        # Adding field 'MuteList.word'
        db.add_column('api_mutelist', 'word',
                      self.gf('django.db.models.fields.URLField')(max_length=300, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'MuteList.domain'
        db.add_column('api_mutelist', 'domain',
                      self.gf('django.db.models.fields.URLField')(default=None, max_length=300),
                      keep_default=False)

        # Deleting field 'MuteList.url'
        db.delete_column('api_mutelist', 'url')

        # Deleting field 'MuteList.word'
        db.delete_column('api_mutelist', 'word')

        # Adding unique constraint on 'MuteList', fields ['user', 'domain']
        db.create_unique('api_mutelist', ['user_id', 'domain'])


    models = {
        'api.blacklistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'BlackListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.chatmessage': {
            'Meta': {'object_name': 'ChatMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        'api.eyehistory': {
            'Meta': {'object_name': 'EyeHistory'},
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'end_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'humanize_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.eyehistorymessage': {
            'Meta': {'ordering': "['-post_time']", 'object_name': 'EyeHistoryMessage'},
            'eyehistory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.EyeHistory']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'api.eyehistoryraw': {
            'Meta': {'object_name': 'EyeHistoryRaw'},
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'end_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'humanize_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.mutelist': {
            'Meta': {'object_name': 'MuteList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'word': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True'})
        },
        'api.popularhistory': {
            'Meta': {'unique_together': "(('user', 'popular_history'),)", 'object_name': 'PopularHistory'},
            'avg_time_ago': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avg_time_spent_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'eye_hists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['api.EyeHistory']", 'symmetrical': 'False'}),
            'humanize_avg_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['api.EyeHistoryMessage']", 'symmetrical': 'False'}),
            'num_comment_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'popular_history': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.PopularHistoryInfo']"}),
            'top_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_time_ago': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_time_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unique_visitor_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'visitors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pophist_visitors'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'api.popularhistoryinfo': {
            'Meta': {'object_name': 'PopularHistoryInfo'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '100'}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'})
        },
        'api.tag': {
            'Meta': {'object_name': 'Tag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.whitelistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'WhiteListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
        }
    }

    complete_apps = ['api']