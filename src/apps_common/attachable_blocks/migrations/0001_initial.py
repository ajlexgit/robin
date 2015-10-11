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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(help_text='For inner use', max_length=128, verbose_name='label')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('block_content_type', models.ForeignKey(null=True, related_name='+', to='contenttypes.ContentType', editable=False)),
            ],
            options={
                'verbose_name_plural': 'attachable blocks',
                'verbose_name': 'attachable block',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('set_name', models.CharField(max_length=32, verbose_name='set name', default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', related_name='references', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
            ],
            options={
                'verbose_name_plural': 'attached blocks',
                'verbose_name': 'attached block',
                'ordering': ('set_name', 'sort_order'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='attachablereference',
            unique_together=set([('content_type', 'object_id', 'block', 'set_name')]),
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
