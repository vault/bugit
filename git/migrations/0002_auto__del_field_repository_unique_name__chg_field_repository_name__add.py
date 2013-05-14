# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Repository.unique_name'
        db.delete_column('git_repository', 'unique_name')


        # Changing field 'Repository.name'
        db.alter_column('git_repository', 'name', self.gf('django.db.models.fields.SlugField')(max_length=100))
        # Adding index on 'Repository', fields ['name']
        db.create_index('git_repository', ['name'])

        # Adding unique constraint on 'Repository', fields ['owner', 'name']
        db.create_unique('git_repository', ['owner_id', 'name'])


        # Changing field 'PublicKey.description'
        db.alter_column('git_publickey', 'description', self.gf('django.db.models.fields.SlugField')(max_length=100))
        # Adding index on 'PublicKey', fields ['description']
        db.create_index('git_publickey', ['description'])

        # Adding unique constraint on 'PublicKey', fields ['owner', 'description']
        db.create_unique('git_publickey', ['owner_id', 'description'])


    def backwards(self, orm):
        # Removing unique constraint on 'PublicKey', fields ['owner', 'description']
        db.delete_unique('git_publickey', ['owner_id', 'description'])

        # Removing index on 'PublicKey', fields ['description']
        db.delete_index('git_publickey', ['description'])

        # Removing unique constraint on 'Repository', fields ['owner', 'name']
        db.delete_unique('git_repository', ['owner_id', 'name'])

        # Removing index on 'Repository', fields ['name']
        db.delete_index('git_repository', ['name'])


        # User chose to not deal with backwards NULL issues for 'Repository.unique_name'
        raise RuntimeError("Cannot reverse this migration. 'Repository.unique_name' and its values cannot be restored.")

        # Changing field 'Repository.name'
        db.alter_column('git_repository', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'PublicKey.description'
        db.alter_column('git_publickey', 'description', self.gf('django.db.models.fields.CharField')(max_length=100))

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
        'git.publickey': {
            'Meta': {'unique_together': "(('owner', 'description'),)", 'object_name': 'PublicKey'},
            'description': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pubkey': ('django.db.models.fields.TextField', [], {})
        },
        'git.repository': {
            'Meta': {'unique_together': "(('owner', 'name'),)", 'object_name': 'Repository'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'collaborator_set'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_set'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['git']