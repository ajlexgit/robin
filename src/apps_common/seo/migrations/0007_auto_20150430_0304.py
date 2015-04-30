# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0006_auto_20150430_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='seodata',
            name='description',
            field=models.CharField(verbose_name='description', blank=True, max_length=160),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seodata',
            name='keywords',
            field=models.CharField(verbose_name='keywords', blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seodata',
            name='title',
            field=models.CharField(verbose_name='title', default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoconfig',
            name='description',
            field=models.CharField(verbose_name='site description', blank=True, max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seoconfig',
            name='keywords',
            field=models.CharField(verbose_name='site keywords', blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seoconfig',
            name='title',
            field=models.CharField(verbose_name='site title', max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seodata',
            name='text',
            field=models.TextField(verbose_name='text', blank=True),
            preserve_default=True,
        ),
    ]
