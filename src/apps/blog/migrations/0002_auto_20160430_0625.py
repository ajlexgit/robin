# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogconfig',
            name='microdata_author',
            field=models.CharField(verbose_name='author', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='blogconfig',
            name='microdata_publisher_logo',
            field=models.ImageField(verbose_name='logo', default='', storage=libs.media_storage.MediaStorage('microdata'), upload_to=''),
            preserve_default=False,
        ),
    ]
