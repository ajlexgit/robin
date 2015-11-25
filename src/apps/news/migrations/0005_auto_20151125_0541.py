# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_post_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=libs.stdimage.fields.StdImageField(verbose_name='preview', upload_to='', aspects=('normal',), storage=libs.media_storage.MediaStorage('news/posts'), blank=True, min_dimensions=(800, 600), variations={'wide': {'size': (800, 600)}, 'micro': {'size': (40, 30)}, 'normal': {'size': (400, 300)}}),
        ),
    ]
