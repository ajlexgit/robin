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
                ('block_type', models.CharField(verbose_name='block type', max_length=255, editable=False)),
                ('label', models.CharField(verbose_name='label', max_length=128, help_text='For inner use')),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Attachable block',
                'verbose_name_plural': 'Attachable blocks',
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachableBlockRef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(verbose_name='block type', max_length=255)),
                ('order', models.PositiveIntegerField(verbose_name='order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Block reference',
                'verbose_name_plural': 'Block references',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block')]),
        ),
    ]
