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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('order', models.PositiveIntegerField(verbose_name='order', default=0)),
                ('created', models.DateTimeField(verbose_name='created on')),
                ('changed', models.DateTimeField(verbose_name='changed on', auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', help_text='Для выборки элементов определенного типа', related_name='+')),
            ],
            options={
                'verbose_name': 'gallery item',
                'verbose_name_plural': 'gallery items',
                'ordering': ('object_id', 'order', 'created'),
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
