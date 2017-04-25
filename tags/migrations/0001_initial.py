# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Highlight'
        db.create_table('tags_highlight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('highlight', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Page'])),
        ))
        db.send_create_signal('tags', ['Highlight'])

        # Adding model 'TagCollection'
        db.create_table('tags_tagcollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('trie_blob', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tags', ['TagCollection'])

        # Adding M2M table for field subscribers on 'TagCollection'
        m2m_table_name = db.shorten_name('tags_tagcollection_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tagcollection', models.ForeignKey(orm['tags.tagcollection'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tagcollection_id', 'user_id'])

        # Adding model 'CommonTag'
        db.create_table('tags_commontag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=10000)),
            ('tag_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.TagCollection'], null=True, blank=True)),
        ))
        db.send_create_signal('tags', ['CommonTag'])

        # Adding M2M table for field subscribers on 'CommonTag'
        m2m_table_name = db.shorten_name('tags_commontag_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('commontag', models.ForeignKey(orm['tags.commontag'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['commontag_id', 'user_id'])

       # Adding model 'Tag'
        db.add_column('tags_tag', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=10000), keep_default=False)
        db.add_column('tags_tag', 'is_private', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
        db.add_column('tags_tag', 'position', self.gf('django.db.models.fields.SmallIntegerField')(null=True), keep_default=False)
        db.add_column('tags_tag', 'page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Page'], null=True), keep_default=False)
        db.add_column('tags_tag', 'domain_obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Domain'], null=True), keep_default=False)
        db.add_column('tags_tag', 'highlight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Highlight'], null=True), keep_default=False)
        db.add_column('tags_tag', 'common_tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.CommonTag'], null=True, blank=True), keep_default=False)
        db.add_column('tags_tag', 'tag_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.TagCollection'], null=True, blank=True), keep_default=False)

        db.alter_column('tags_tag', 'color', self.gf('django.db.models.fields.CharField')(max_length=10))
        db.alter_column('tags_tag', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='creator', null=True, to=orm['auth.User']))

        # Adding M2M table for field subscribers on 'Tag'
        m2m_table_name = db.shorten_name('tags_tag_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['tags.tag'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'user_id'])

        # Adding model 'Vote'
        db.create_table('tags_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Tag'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('tags', ['Vote'])

        # Adding model 'UserTagInfo'
        db.create_table('tags_usertaginfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Page'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Tag'])),
        ))
        db.send_create_signal('tags', ['UserTagInfo'])


    def backwards(self, orm):
        # Deleting model 'Highlight'
        db.delete_table('tags_highlight')

        # Deleting model 'TagCollection'
        db.delete_table('tags_tagcollection')

        # Removing M2M table for field subscribers on 'TagCollection'
        db.delete_table(db.shorten_name('tags_tagcollection_subscribers'))

        # Deleting model 'CommonTag'
        db.delete_table('tags_commontag')

        # Removing M2M table for field subscribers on 'CommonTag'
        db.delete_table(db.shorten_name('tags_commontag_subscribers'))

        # Removing M2M table for field subscribers on 'Tag'
        db.delete_table(db.shorten_name('tags_tag_subscribers'))

        # Deleting model 'Vote'
        db.delete_table('tags_vote')

        # Deleting model 'UserTagInfo'
        db.delete_table('tags_usertaginfo')

        db.delete_column('tags_tag', 'description')
        db.delete_column('tags_tag', 'is_private')
        db.delete_column('tags_tag', 'position')
        db.delete_column('tags_tag', 'page')
        db.delete_column('tags_tag', 'domain_obj')
        db.delete_column('tags_tag', 'highlight')
        db.delete_column('tags_tag', 'common_tag')
        db.delete_column('tags_tag', 'tag_collection')

        db.alter_column('tags_tag', 'color', self.gf('django.db.models.fields.CharField')(default=0, max_length=10))
        db.alter_column('tags_tag', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))


    models = {
        'api.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        'api.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Domain']"}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
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
        'tags.commontag': {
            'Meta': {'object_name': 'CommonTag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'tag_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.TagCollection']", 'null': 'True', 'blank': 'True'})
        },
        'tags.highlight': {
            'Meta': {'object_name': 'Highlight'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highlight': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Page']"})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'common_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.CommonTag']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10000'}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '300'}),
            'domain_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Domain']", 'null': 'True'}),
            'highlight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Highlight']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Page']", 'null': 'True'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribers'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'tag_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.TagCollection']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'tags.tagcollection': {
            'Meta': {'object_name': 'TagCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'trie_blob': ('django.db.models.fields.TextField', [], {})
        },
        'tags.usertaginfo': {
            'Meta': {'object_name': 'UserTagInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Page']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tags.vote': {
            'Meta': {'object_name': 'Vote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Tag']"}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['auth', 'tags']