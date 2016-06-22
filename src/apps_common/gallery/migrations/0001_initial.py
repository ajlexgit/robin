# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItemBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('created', models.DateTimeField(verbose_name='created on', blank=True)),
                ('changed', models.DateTimeField(verbose_name='changed on', auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(to='contenttypes.ContentType', editable=False, related_name='+', help_text='Для выборки элементов определенного типа')),
            ],
            options={
                'verbose_name': 'gallery item',
                'verbose_name_plural': 'gallery items',
                'ordering': ('object_id', 'sort_order', 'created'),
                'default_permissions': (),
            },
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
