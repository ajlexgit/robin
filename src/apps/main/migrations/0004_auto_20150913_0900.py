# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_mainpageconfig_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='video',
            field=libs.videolink_field.fields.VideoLinkField(verbose_name='video', blank=True),
            preserve_default=True,
        ),
    ]
