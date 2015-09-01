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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('block_type', models.CharField(editable=False, verbose_name='block type', max_length=255)),
                ('label', models.CharField(help_text='For inner use', verbose_name='label', max_length=128)),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name_plural': 'Attachable blocks',
                'verbose_name': 'Attachable block',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableBlockRef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(verbose_name='block type', max_length=255)),
                ('frame', models.PositiveSmallIntegerField(default=0, verbose_name='frame')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('frame', 'order'),
                'verbose_name_plural': 'Block references',
                'verbose_name': 'Block reference',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block')]),
        ),
    ]
