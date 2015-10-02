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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('block_type', models.CharField(verbose_name='block type', max_length=255, editable=False)),
                ('label', models.CharField(verbose_name='label', max_length=128, help_text='For inner use')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'Attachable block',
                'verbose_name_plural': 'Attachable blocks',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(verbose_name='block type', max_length=255)),
                ('set_name', models.CharField(default='default', verbose_name='set name', max_length=32)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', related_name='references', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('set_name', 'sort_order'),
                'verbose_name': 'Attached block',
                'verbose_name_plural': 'Attached blocks',
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
