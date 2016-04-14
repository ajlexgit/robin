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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=128, verbose_name='label', help_text='For inner use')),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('block_content_type', models.ForeignKey(related_name='+', null=True, to='contenttypes.ContentType', editable=False)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'attachable blocks',
                'verbose_name': 'attachable block',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('noindex', models.BooleanField(default=True, verbose_name='noIndex', help_text='wraps block with &lt;!--noidex--&gt;')),
                ('ajax', models.BooleanField(default=False, verbose_name='AJAX load', help_text='load block through AJAX')),
                ('set_name', models.CharField(default='default', verbose_name='set name', max_length=32)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(related_name='references', verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'attached blocks',
                'verbose_name': 'attached block',
                'ordering': ('set_name', 'sort_order'),
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
