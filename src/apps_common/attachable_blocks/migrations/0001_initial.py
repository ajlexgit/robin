# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachableBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('block_type', models.CharField(verbose_name='block type', editable=False, max_length=255)),
                ('label', models.CharField(verbose_name='label', help_text='For inner use', max_length=128)),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'attachable blocks',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(verbose_name='block type', max_length=255)),
                ('set_name', models.CharField(default='default', verbose_name='set name', max_length=32)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', verbose_name='block', related_name='references')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'attached block',
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'attached blocks',
            },
        ),
        migrations.AlterUniqueTogether(
            name='attachablereference',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block', 'set_name')]),
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
