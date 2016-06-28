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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('label', models.CharField(verbose_name='label', help_text='For inner use', max_length=128)),
                ('visible', models.BooleanField(verbose_name='visible', default=True)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('block_content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', related_name='+', null=True)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'attachable block',
                'default_permissions': (),
                'verbose_name_plural': 'attachable blocks',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('ajax', models.BooleanField(verbose_name='AJAX load', help_text='load block through AJAX', default=False)),
                ('set_name', models.CharField(verbose_name='set name', max_length=32, default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', to='attachable_blocks.AttachableBlock', related_name='references')),
                ('block_ct', models.ForeignKey(to='contenttypes.ContentType', related_name='+', null=True)),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('set_name', 'sort_order'),
                'verbose_name': 'attached block',
                'verbose_name_plural': 'attached blocks',
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
