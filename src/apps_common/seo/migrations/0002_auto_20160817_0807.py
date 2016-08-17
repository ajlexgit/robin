# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoconfig',
            name='description',
            field=models.TextField(verbose_name='meta description', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seoconfig',
            name='keywords',
            field=models.TextField(verbose_name='meta keywords', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seoconfig',
            name='title',
            field=models.CharField(verbose_name='meta title', max_length=128),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='description',
            field=models.TextField(verbose_name='meta description', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='keywords',
            field=models.TextField(verbose_name='meta keywords', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='title',
            field=models.CharField(verbose_name='meta title', max_length=128, blank=True),
        ),
    ]
