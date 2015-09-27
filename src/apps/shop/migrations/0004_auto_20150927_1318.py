# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import libs.valute_field.fields
import django.core.validators
import libs.stdimage.fields
import libs.media_storage
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150927_1314'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='ShopProduct'
        ),
    ]
