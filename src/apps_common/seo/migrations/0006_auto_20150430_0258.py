# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('seo', '0005_auto_20150428_0530'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'SEO records',
                'verbose_name': 'SEO record',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='seotext',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='seotext',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='SeoText',
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
