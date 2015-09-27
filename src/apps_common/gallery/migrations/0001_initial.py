# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItemBase',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('created', models.DateTimeField(verbose_name='created on')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='changed on')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', editable=False, help_text='Для выборки элементов определенного типа')),
            ],
            options={
                'verbose_name_plural': 'gallery items',
                'verbose_name': 'gallery item',
                'ordering': ('object_id', 'sort_order', 'created'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
