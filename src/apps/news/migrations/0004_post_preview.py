# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20151125_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='preview',
            field=libs.stdimage.fields.StdImageField(upload_to='', verbose_name='preview', variations={'wide': {'size': (800, 600)}, 'normal': {'size': (400, 300)}}, aspects=('normal',), blank=True, min_dimensions=(800, 600), storage=libs.media_storage.MediaStorage('news')),
        ),
    ]
