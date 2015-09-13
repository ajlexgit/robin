# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150909_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='video',
            field=libs.videolink_field.fields.VideoLinkField(verbose_name='video', default=''),
            preserve_default=False,
        ),
    ]
