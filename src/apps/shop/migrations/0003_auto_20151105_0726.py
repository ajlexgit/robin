# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models
import django.db.models.deletion
import gallery.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('shop', '0002_auto_20151102_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopProductGallery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, to='gallery.GalleryItemBase', auto_created=True)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, editable=False, verbose_name='stored_crop', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.ShopProductGallery', null=True, verbose_name='gallery'),
        ),
    ]
