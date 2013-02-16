# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'builder_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('altPhone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('altDegree', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('altInfo', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'builder', ['UserProfile'])

        # Adding model 'Project'
        db.create_table(u'builder_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['builder.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('projectURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('inDevelopment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isPublic', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('projectImage', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('highlight', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'builder', ['Project'])

        # Adding model 'WorkExperience'
        db.create_table(u'builder_workexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jobTitle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('startDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('supervisorName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('supervisorEmail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['builder.UserProfile'])),
        ))
        db.send_create_signal(u'builder', ['WorkExperience'])

        # Adding model 'VolunteerExperience'
        db.create_table(u'builder_volunteerexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('jobTitle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('startDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('supervisorName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('supervisorEmail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['builder.UserProfile'])),
        ))
        db.send_create_signal(u'builder', ['VolunteerExperience'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'builder_userprofile')

        # Deleting model 'Project'
        db.delete_table(u'builder_project')

        # Deleting model 'WorkExperience'
        db.delete_table(u'builder_workexperience')

        # Deleting model 'VolunteerExperience'
        db.delete_table(u'builder_volunteerexperience')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'builder.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inDevelopment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isPublic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'projectImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'projectURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.UserProfile']"})
        },
        u'builder.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'altDegree': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'altInfo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'altPhone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'builder.volunteerexperience': {
            'Meta': {'object_name': 'VolunteerExperience'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'endDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobTitle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'startDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'supervisorEmail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'supervisorName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.UserProfile']"})
        },
        u'builder.workexperience': {
            'Meta': {'object_name': 'WorkExperience'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'endDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobTitle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'startDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'supervisorEmail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'supervisorName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.UserProfile']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['builder']