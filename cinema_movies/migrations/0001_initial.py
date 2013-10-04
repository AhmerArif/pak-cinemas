# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table(u'cinema_movies_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('long_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
        ))
        db.send_create_signal(u'cinema_movies', ['City'])

        # Adding model 'Cinema'
        db.create_table(u'cinema_movies_cinema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinema_movies.City'])),
        ))
        db.send_create_signal(u'cinema_movies', ['Cinema'])

        # Adding model 'Movie'
        db.create_table(u'cinema_movies_movie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('imdb_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('rotten_tomatoes_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'cinema_movies', ['Movie'])

        # Adding model 'Showtime'
        db.create_table(u'cinema_movies_showtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinema_movies.Movie'])),
            ('cinema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinema_movies.Cinema'])),
            ('showing_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('show_3d_or_2d', self.gf('django.db.models.fields.CharField')(default='2D', max_length=3)),
            ('show_adults_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cinema_movies', ['Showtime'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table(u'cinema_movies_city')

        # Deleting model 'Cinema'
        db.delete_table(u'cinema_movies_cinema')

        # Deleting model 'Movie'
        db.delete_table(u'cinema_movies_movie')

        # Deleting model 'Showtime'
        db.delete_table(u'cinema_movies_showtime')


    models = {
        u'cinema_movies.cinema': {
            'Meta': {'object_name': 'Cinema'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cinema_movies.City']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'cinema_movies.city': {
            'Meta': {'object_name': 'City'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cinema_movies.movie': {
            'Meta': {'object_name': 'Movie'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'rotten_tomatoes_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cinema_movies.showtime': {
            'Meta': {'object_name': 'Showtime'},
            'cinema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cinema_movies.Cinema']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cinema_movies.Movie']"}),
            'show_3d_or_2d': ('django.db.models.fields.CharField', [], {'default': "'2D'", 'max_length': '3'}),
            'show_adults_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'showing_at': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cinema_movies']