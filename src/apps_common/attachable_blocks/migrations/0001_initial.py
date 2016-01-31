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
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('block_content_type', models.ForeignKey(null=True, related_name='+', editable=False, to='contenttypes.ContentType')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('noindex', models.BooleanField(verbose_name='noIndex', help_text='wraps block with &lt;!--noidex--&gt;', default=True)),
                ('ajax', models.BooleanField(verbose_name='AJAX load', help_text='load block with AJAX', default=False)),
                ('set_name', models.CharField(verbose_name='set name', max_length=32, default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', related_name='references', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
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
