# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import gallery.models
import libs.media_storage
import django.db.models.deletion
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(max_length=32, verbose_name='stored_crop', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('preview', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(800, 600), storage=libs.media_storage.MediaStorage('main'), variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, verbose_name='preview', aspects=('normal',), blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, to='main.Gallery', null=True, verbose_name='gallery', blank=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
    ]
