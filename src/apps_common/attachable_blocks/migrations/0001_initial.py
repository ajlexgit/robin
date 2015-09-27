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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], verbose_name='block type', max_length=255, editable=False)),
                ('label', models.CharField(verbose_name='label', max_length=128, help_text='For inner use')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Attachable block',
                'verbose_name_plural': 'Attachable blocks',
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], verbose_name='block type', max_length=255)),
                ('set_name', models.CharField(verbose_name='set name', max_length=32, default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(related_name='references', verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Attached block',
                'verbose_name_plural': 'Attached blocks',
                'ordering': ('set_name', 'sort_order'),
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
