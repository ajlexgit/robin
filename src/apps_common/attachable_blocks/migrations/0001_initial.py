# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachableBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=128, verbose_name='label', help_text='For inner use')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('block_content_type', models.ForeignKey(editable=False, null=True, related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'attachable block',
                'verbose_name_plural': 'attachable blocks',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('noindex', models.BooleanField(verbose_name='noIndex', default=True, help_text='wraps block with &lt;!--noidex--&gt;')),
                ('ajax', models.BooleanField(verbose_name='AJAX load', default=False, help_text='load block with AJAX')),
                ('set_name', models.CharField(max_length=32, verbose_name='set name', default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', related_name='references', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'attached block',
                'verbose_name_plural': 'attached blocks',
                'ordering': ('set_name', 'sort_order'),
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
