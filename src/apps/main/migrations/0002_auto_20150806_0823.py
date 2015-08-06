# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, serialize=False, to='attachable_blocks.AttachableBlock', parent_link=True, auto_created=True)),
            ],
            options={
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, serialize=False, to='attachable_blocks.AttachableBlock', parent_link=True, auto_created=True)),
            ],
            options={
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainPageBlockRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_model', models.CharField(verbose_name='block model', max_length=255)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', verbose_name='block')),
                ('page', models.ForeignKey(to='main.MainPageConfig')),
            ],
            options={
                'verbose_name_plural': 'Block references',
                'abstract': False,
                'verbose_name': 'Block reference',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='mainpageblockref',
            unique_together=set([('block_model', 'page')]),
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='blocks',
            field=models.ManyToManyField(to='attachable_blocks.AttachableBlock', through='main.MainPageBlockRef'),
            preserve_default=True,
        ),
    ]
