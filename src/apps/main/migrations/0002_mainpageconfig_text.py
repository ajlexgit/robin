# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='text',
            field=libs.ckeditor.fields.CKEditorUploadField(default='', verbose_name='text'),
            preserve_default=False,
        ),
    ]
