# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.fields
import django.db.models.deletion
import libs.media_storage
import libs.videolink_field.fields
import gallery.models
import libs.valute_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'default_permissions': (),
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='gallery.GalleryItemBase', primary_key=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('image_crop', models.CharField(blank=True, max_length=32, editable=False, verbose_name='stored_crop')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'image items',
                'default_permissions': (),
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Gallery', null=True, verbose_name='gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='gallery.GalleryItemBase', primary_key=True, serialize=False)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(blank=True, storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='preview')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'video items',
                'default_permissions': (),
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
