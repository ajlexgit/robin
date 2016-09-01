# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0003_seodata_noindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seodata',
            name='description',
            field=models.TextField(verbose_name='description', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='keywords',
            field=models.TextField(verbose_name='keywords', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='noindex',
            field=models.BooleanField(help_text='the text on the page will not be indexed', verbose_name='noindex', default=False),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='title',
            field=models.CharField(verbose_name='title', blank=True, max_length=128),
        ),
    ]
