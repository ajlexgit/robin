# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import libs.media_storage
import gallery.models
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'abstract': False,
                'verbose_name_plural': 'galleries',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', editable=False, blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'abstract': False,
                'verbose_name_plural': 'image items',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
    ]
