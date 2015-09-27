# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='gallery2',
            field=gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, related_name='page2', verbose_name='gallery2', blank=True, to='main.MainGallery', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='gallery',
            field=gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, related_name='page', verbose_name='gallery', blank=True, to='main.MainGallery', null=True),
            preserve_default=True,
        ),
    ]
