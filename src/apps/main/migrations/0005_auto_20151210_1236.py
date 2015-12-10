# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.fields
import libs.media_storage
import gallery.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('main', '0004_remove_mainpageconfig_coords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', auto_created=True, parent_link=True, primary_key=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(blank=True, verbose_name='stored_crop', max_length=32, editable=False)),
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
            field=gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='main.Gallery', verbose_name='gallery'),
        ),
    ]
