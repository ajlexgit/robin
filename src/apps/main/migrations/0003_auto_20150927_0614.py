# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150927_0541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='gallery2',
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='gallery',
            field=gallery.fields.GalleryField(verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, null=True, to='main.MainGallery', blank=True),
            preserve_default=True,
        ),
    ]
