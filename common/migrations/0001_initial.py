# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicKey'
        db.create_table('common_publickey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('pubkey', self.gf('django.db.models.fields.TextField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['PublicKey'])

        # Adding unique constraint on 'PublicKey', fields ['owner', 'description']
        db.create_unique('common_publickey', ['owner_id', 'description'])

        # Adding model 'Repository'
        db.create_table('common_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_set', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['Repository'])

        # Adding unique constraint on 'Repository', fields ['owner', 'name']
        db.create_unique('common_repository', ['owner_id', 'name'])

        # Adding model 'Collaboration'
        db.create_table('common_collaboration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Repository'])),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('common', ['Collaboration'])

        # Adding unique constraint on 'Collaboration', fields ['user', 'repository']
        db.create_unique('common_collaboration', ['user_id', 'repository_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Collaboration', fields ['user', 'repository']
        db.delete_unique('common_collaboration', ['user_id', 'repository_id'])

        # Removing unique constraint on 'Repository', fields ['owner', 'name']
        db.delete_unique('common_repository', ['owner_id', 'name'])

        # Removing unique constraint on 'PublicKey', fields ['owner', 'description']
        db.delete_unique('common_publickey', ['owner_id', 'description'])

        # Deleting model 'PublicKey'
        db.delete_table('common_publickey')

        # Deleting model 'Repository'
        db.delete_table('common_repository')

        # Deleting model 'Collaboration'
        db.delete_table('common_collaboration')


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
        'common.collaboration': {
            'Meta': {'unique_together': "(('user', 'repository'),)", 'object_name': 'Collaboration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Repository']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.publickey': {
            'Meta': {'unique_together': "(('owner', 'description'),)", 'object_name': 'PublicKey'},
            'description': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pubkey': ('django.db.models.fields.TextField', [], {})
        },
        'common.repository': {
            'Meta': {'unique_together': "(('owner', 'name'),)", 'object_name': 'Repository'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'collaborator_set'", 'blank': 'True', 'through': "orm['common.Collaboration']", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_set'", 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']