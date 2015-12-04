# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='preview',
            field=libs.stdimage.fields.StdImageField(aspects=('normal',), upload_to='', storage=libs.media_storage.MediaStorage('main'), variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, blank=True, verbose_name='preview'),
        ),
    ]
