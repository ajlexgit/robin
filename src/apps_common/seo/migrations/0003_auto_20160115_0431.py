# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_auto_20160115_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='seodata',
            name='og_description',
            field=models.TextField(blank=True, verbose_name='description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seodata',
            name='og_image',
            field=models.ImageField(blank=True, verbose_name='image', upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seodata',
            name='og_title',
            field=models.CharField(max_length=255, blank=True, verbose_name='title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='counter',
            name='label',
            field=models.CharField(max_length=128, verbose_name='label'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='counter',
            name='position',
            field=models.CharField(max_length=12, choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], verbose_name='position'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seodata',
            name='header',
            field=models.CharField(max_length=128, blank=True, verbose_name='header'),
            preserve_default=True,
        ),
    ]
