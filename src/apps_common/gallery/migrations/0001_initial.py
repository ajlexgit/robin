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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('created', models.DateTimeField(verbose_name='created on')),
                ('changed', models.DateTimeField(verbose_name='changed on', auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', related_name='+', help_text='Для выборки элементов определенного типа')),
            ],
            options={
                'ordering': ('object_id', 'order', 'created'),
                'verbose_name': 'gallery item',
                'verbose_name_plural': 'gallery items',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
