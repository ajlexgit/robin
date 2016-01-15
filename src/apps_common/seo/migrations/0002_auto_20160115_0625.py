# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seodata',
            name='og_description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='seodata',
            name='og_image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='image'),
        ),
        migrations.AddField(
            model_name='seodata',
            name='og_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='title'),
        ),
    ]
