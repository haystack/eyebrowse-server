# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table('api_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Tag'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('api', ['Vote'])

        # Adding model 'BaseTag'
        db.create_table('api_basetag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('domain', self.gf('django.db.models.fields.URLField')(default='', max_length=300)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=10000)),
        ))
        db.send_create_signal('api', ['BaseTag'])

        # Adding model 'Topic'
        db.create_table('api_topic', (
            ('tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['api.Tag'], unique=True, primary_key=True)),
            ('position', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
        ))
        db.send_create_signal('api', ['Topic'])

        # Adding model 'Value'
        db.create_table('api_value', (
            ('tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['api.Tag'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('api', ['Value'])

        # Adding model 'UserTagInfo'
        db.create_table('api_usertaginfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Page'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Tag'])),
        ))
        db.send_create_signal('api', ['UserTagInfo'])

        # Deleting field 'Tag.domain'
        db.delete_column('api_tag', 'domain')

        # Deleting field 'Tag.name'
        db.delete_column('api_tag', 'name')

        # Deleting field 'Tag.color'
        db.delete_column('api_tag', 'color')

        # Adding field 'Tag.is_private'
        db.add_column('api_tag', 'is_private',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Tag.page'
        db.add_column('api_tag', 'page',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Page'], null=True),
                      keep_default=False)

        # Adding field 'Tag.domain_obj'
        db.add_column('api_tag', 'domain_obj',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Domain'], null=True),
                      keep_default=False)

        # Adding field 'Tag.vote_count'
        db.add_column('api_tag', 'vote_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Tag.highlight'
        db.add_column('api_tag', 'highlight',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Highlight'], null=True),
                      keep_default=False)

        # Adding field 'Tag.base_tag'
        db.add_column('api_tag', 'base_tag',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['api.BaseTag']),
                      keep_default=False)


        # Changing field 'Tag.user'
        db.alter_column('api_tag', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))
        # Adding field 'PopularHistoryInfo.page'
        db.add_column('api_popularhistoryinfo', 'page',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Page'], null=True, on_delete=models.SET_NULL),
                      keep_default=False)

        # Adding field 'EyeHistory.page'
        db.add_column('api_eyehistory', 'page',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Page'], null=True, on_delete=models.SET_NULL),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table('api_vote')

        # Deleting model 'BaseTag'
        db.delete_table('api_basetag')

        # Deleting model 'Topic'
        db.delete_table('api_topic')

        # Deleting model 'Value'
        db.delete_table('api_value')

        # Deleting model 'UserTagInfo'
        db.delete_table('api_usertaginfo')

        # Adding field 'Tag.domain'
        db.add_column('api_tag', 'domain',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=300),
                      keep_default=False)

        # Adding field 'Tag.name'
        db.add_column('api_tag', 'name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'Tag.color'
        db.add_column('api_tag', 'color',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Deleting field 'Tag.is_private'
        db.delete_column('api_tag', 'is_private')

        # Deleting field 'Tag.page'
        db.delete_column('api_tag', 'page_id')

        # Deleting field 'Tag.domain_obj'
        db.delete_column('api_tag', 'domain_obj_id')

        # Deleting field 'Tag.vote_count'
        db.delete_column('api_tag', 'vote_count')

        # Deleting field 'Tag.highlight'
        db.delete_column('api_tag', 'highlight_id')

        # Deleting field 'Tag.base_tag'
        db.delete_column('api_tag', 'base_tag_id')


        # Changing field 'Tag.user'
        db.alter_column('api_tag', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']))
        # Deleting field 'PopularHistoryInfo.page'
        db.delete_column('api_popularhistoryinfo', 'page_id')

        # Deleting field 'EyeHistory.page'
        db.delete_column('api_eyehistory', 'page_id')


    models = {
        'api.basetag': {
            'Meta': {'object_name': 'BaseTag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10000'}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'api.blacklistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'BlackListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
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
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'humanize_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Page']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
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
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Page']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'})
        },
        'api.tag': {
            'Meta': {'object_name': 'Tag'},
            'base_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.BaseTag']"}),
            'domain_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Domain']", 'null': 'True'}),
            'highlight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Highlight']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Page']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'api.topic': {
            'Meta': {'object_name': 'Topic', '_ormbases': ['api.Tag']},
            'position': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['api.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        'api.usertaginfo': {
            'Meta': {'object_name': 'UserTagInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Page']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.value': {
            'Meta': {'object_name': 'Value', '_ormbases': ['api.Tag']},
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['api.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        'api.vote': {
            'Meta': {'object_name': 'Vote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Tag']"}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.whitelistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'WhiteListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2017, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
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
        },
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

    complete_apps = ['api']