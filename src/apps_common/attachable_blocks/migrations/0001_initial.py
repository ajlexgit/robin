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
                ('block_type', models.CharField(editable=False, max_length=255, verbose_name='block type')),
                ('label', models.CharField(help_text='For inner use', max_length=128, verbose_name='label')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name_plural': 'Attachable blocks',
                'ordering': ('label',),
                'verbose_name': 'Attachable block',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableBlockRef',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(max_length=255, verbose_name='block type')),
                ('frame', models.PositiveSmallIntegerField(default=0, verbose_name='frame')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Block references',
                'ordering': ('frame', 'order'),
                'verbose_name': 'Block reference',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block')]),
        ),
    ]
