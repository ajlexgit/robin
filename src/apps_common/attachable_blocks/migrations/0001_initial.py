# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachableBlock',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('block_type', models.CharField(max_length=255, editable=False, verbose_name='block type')),
                ('label', models.CharField(max_length=128, help_text='For inner use', verbose_name='label')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name_plural': 'Attachable blocks',
                'verbose_name': 'Attachable block',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(max_length=255, verbose_name='block type')),
                ('set_name', models.CharField(max_length=32, verbose_name='set name', default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', related_name='references', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'Attached blocks',
                'verbose_name': 'Attached block',
            },
            bases=(models.Model,),
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
