# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Drug'
        db.create_table(u'drugs_drug', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('generic_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'drugs', ['Drug'])


    def backwards(self, orm):
        # Deleting model 'Drug'
        db.delete_table(u'drugs_drug')


    models = {
        u'drugs.drug': {
            'Meta': {'object_name': 'Drug'},
            'generic_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['drugs']