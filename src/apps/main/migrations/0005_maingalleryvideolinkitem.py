# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('main', '0004_auto_20150913_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, to='gallery.GalleryItemBase', parent_link=True, primary_key=True, auto_created=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video')),
                ('video_preview', models.CharField(verbose_name='preview image', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'verbose_name_plural': 'video items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
