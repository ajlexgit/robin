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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='For inner use', max_length=128, verbose_name='label')),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', editable=False, null=True)),
            ],
            options={
                'ordering': ('label',),
                'default_permissions': (),
                'verbose_name_plural': 'attachable blocks',
                'verbose_name': 'attachable block',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('ajax', models.BooleanField(help_text='load block via AJAX', default=False, verbose_name='AJAX')),
                ('set_name', models.CharField(max_length=32, default='default', verbose_name='set name')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(related_name='references', to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('block_ct', models.ForeignKey(related_name='+', to='contenttypes.ContentType', null=True)),
                ('content_type', models.ForeignKey(help_text='content type of entity, attached to', related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'attached blocks',
                'verbose_name': 'attached block',
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
