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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('label', models.CharField(help_text='For inner use', max_length=128, verbose_name='label')),
                ('visible', models.BooleanField(verbose_name='visible', default=True)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('block_content_type', models.ForeignKey(related_name='+', null=True, editable=False, to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'attachable blocks',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('noindex', models.BooleanField(help_text='wraps block with &lt;!--noidex--&gt;', verbose_name='noIndex', default=True)),
                ('ajax', models.BooleanField(help_text='load block through AJAX', verbose_name='AJAX load', default=False)),
                ('set_name', models.CharField(verbose_name='set name', max_length=32, default='default')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', default=0)),
                ('block', models.ForeignKey(related_name='references', verbose_name='block', to='attachable_blocks.AttachableBlock')),
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
