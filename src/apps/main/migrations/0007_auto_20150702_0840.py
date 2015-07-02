# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.fields
import libs.checks
import libs.media_storage
import gallery.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('main', '0006_remove_mainpageconfig_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name': 'gallery',
                'abstract': False,
                'verbose_name_plural': 'galleries',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='gallery.GalleryItemBase', parent_link=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', blank=True, null=True, storage=libs.media_storage.MediaStorage())),
                ('crop', models.CharField(verbose_name='image crop coordinates', max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'abstract': False,
                'verbose_name_plural': 'image items',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='gallery',
            field=gallery.fields.GalleryField(verbose_name='gallery', to='main.MainGallery', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
