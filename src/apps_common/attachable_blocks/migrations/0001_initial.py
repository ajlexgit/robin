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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='For inner use', max_length=128, verbose_name='label')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('block_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType', null=True, editable=False)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name_plural': 'attachable blocks',
                'default_permissions': (),
                'verbose_name': 'attachable block',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('noindex', models.BooleanField(help_text='wraps block with &lt;!--noidex--&gt;', default=True, verbose_name='noIndex')),
                ('ajax', models.BooleanField(help_text='load block through AJAX', default=False, verbose_name='AJAX load')),
                ('set_name', models.CharField(max_length=32, default='default', verbose_name='set name')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(related_name='references', to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
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
