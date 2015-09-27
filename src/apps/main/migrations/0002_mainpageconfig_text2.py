# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='text2',
            field=ckeditor.fields.CKEditorUploadField(verbose_name='text2', default=''),
            preserve_default=False,
        ),
    ]
