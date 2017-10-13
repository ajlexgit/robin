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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('created', models.DateTimeField(blank=True, verbose_name='created on')),
                ('changed', models.DateTimeField(verbose_name='changed on', auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('self_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', editable=False)),
            ],
            options={
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'gallery items',
                'verbose_name': 'gallery item',
                'default_permissions': (),
            },
        ),
        migrations.AlterIndexTogether(
            name='galleryitembase',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
