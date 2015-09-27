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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('block_type', models.CharField(max_length=255, editable=False, verbose_name='block type')),
                ('label', models.CharField(max_length=128, verbose_name='label', help_text='For inner use')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name_plural': 'Attachable blocks',
                'verbose_name': 'Attachable block',
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(max_length=255, verbose_name='block type')),
                ('set_name', models.CharField(max_length=32, default='default', verbose_name='set name')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(related_name='references', to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Attached blocks',
                'ordering': ('set_name', 'sort_order'),
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
