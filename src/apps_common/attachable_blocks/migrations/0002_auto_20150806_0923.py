# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachableBlockRef',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('block_model', models.CharField(choices=[('main.models.MainBlockFirst', 'First block type'), ('main.models.MainBlockSecond', 'Second block type')], verbose_name='block model', max_length=255)),
                ('order', models.PositiveIntegerField(verbose_name='order', default=0)),
                ('block', models.ForeignKey(verbose_name='block', to='attachable_blocks.AttachableBlock')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Block reference',
                'ordering': ('order',),
                'verbose_name_plural': 'Block references',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='attachableblock',
            name='block_model',
            field=models.CharField(choices=[('main.models.MainBlockFirst', 'First block type'), ('main.models.MainBlockSecond', 'Second block type')], verbose_name='block model', max_length=255, default='attachable_blocks.models.AttachableBlock', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblock',
            name='created',
            field=models.DateTimeField(verbose_name='create date', editable=False),
            preserve_default=True,
        ),
    ]
