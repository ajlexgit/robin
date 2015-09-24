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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('block_type', models.CharField(choices=[('blocks.mainsliderblock', 'MainSlider Blocks'), ('blocks.suppliersblock', 'Suppliers blocks')], editable=False, verbose_name='block type', max_length=255)),
                ('label', models.CharField(help_text='For inner use', verbose_name='label', max_length=128)),
                ('visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date')),
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
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('block_type', models.CharField(choices=[('blocks.mainsliderblock', 'MainSlider Blocks'), ('blocks.suppliersblock', 'Suppliers blocks')], verbose_name='block type', max_length=255)),
                ('set_name', models.CharField(default='default', verbose_name='set name', max_length=32)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('block', models.ForeignKey(related_name='references', verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('set_name', 'order'),
                'verbose_name_plural': 'Attached blocks',
                'verbose_name': 'Attached block',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachablereference',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block', 'set_name')]),
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
