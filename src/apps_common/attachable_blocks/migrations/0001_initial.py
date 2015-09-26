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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(editable=False, verbose_name='block type', max_length=255)),
                ('label', models.CharField(verbose_name='label', max_length=128, help_text='For inner use')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'Attachable blocks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(verbose_name='block type', max_length=255)),
                ('set_name', models.CharField(verbose_name='set name', default='default', max_length=32)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', related_name='references', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Attached block',
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'Attached blocks',
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
