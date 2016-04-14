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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('created', models.DateTimeField(verbose_name='created on', blank=True)),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='changed on')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', editable=False, help_text='Для выборки элементов определенного типа')),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'gallery items',
                'verbose_name': 'gallery item',
                'ordering': ('object_id', 'sort_order', 'created'),
            },
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
