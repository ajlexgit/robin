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
                ('label', models.CharField(verbose_name='label', help_text='For inner use', max_length=128)),
                ('visible', models.BooleanField(verbose_name='visible', default=True)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('block_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', editable=False, null=True)),
            ],
            options={
                'verbose_name': 'attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'attachable blocks',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('ajax', models.BooleanField(verbose_name='AJAX load', default=False, help_text='load block through AJAX')),
                ('set_name', models.CharField(verbose_name='set name', default='default', max_length=32)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(related_name='references', to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('block_ct', models.ForeignKey(related_name='+', to='contenttypes.ContentType', null=True)),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'attached block',
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'attached blocks',
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
