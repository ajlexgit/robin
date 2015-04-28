# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('seo', '0002_seotext'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seotext',
            options={'verbose_name': 'SEO text', 'verbose_name_plural': 'SEO texts'},
        ),
        migrations.RemoveField(
            model_name='seotext',
            name='url',
        ),
        migrations.AddField(
            model_name='seotext',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seotext',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
