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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('block_type', models.CharField(max_length=255, verbose_name='block type', editable=False)),
                ('label', models.CharField(max_length=128, verbose_name='label', help_text='For inner use')),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'Attachable blocks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableBlockRef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(max_length=255, verbose_name='block type')),
                ('frame', models.PositiveSmallIntegerField(default=0, verbose_name='frame')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('block', models.ForeignKey(verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Block reference',
                'ordering': ('frame', 'order'),
                'verbose_name_plural': 'Block references',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block')]),
        ),
    ]
