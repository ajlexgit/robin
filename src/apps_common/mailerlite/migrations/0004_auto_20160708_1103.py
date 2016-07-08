# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0003_remove_campaign_preheader'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailerconfig',
            name='logo',
            field=models.ImageField(upload_to='', storage=libs.storages.media_storage.MediaStorage('mailerlite/logo'), blank=True, verbose_name='logo'),
        ),
        migrations.AddField(
            model_name='mailerconfig',
            name='preheader',
            field=models.TextField(blank=True, verbose_name='pre-header'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='header_image',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(640, 200), storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), aspects='normal', variations={'normal': {'size': (640, 200), 'quality': 95}, 'admin': {'size': (480, 150)}}, upload_to='', blank=True, verbose_name='preview'),
        ),
    ]
