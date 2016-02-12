# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.videolink_field.fields
import gallery.models
import gallery.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='gallery.GalleryItemBase', serialize=False)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, blank=True, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
            ],
            options={
                'verbose_name_plural': 'video items',
                'abstract': False,
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
