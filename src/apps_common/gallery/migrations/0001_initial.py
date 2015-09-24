# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.checks


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItemBase',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('created', models.DateTimeField(verbose_name='created on')),
                ('changed', models.DateTimeField(verbose_name='changed on', auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(to='contenttypes.ContentType', help_text='Для выборки элементов определенного типа', editable=False, related_name='+')),
            ],
            options={
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'gallery items',
                'verbose_name': 'gallery item',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
