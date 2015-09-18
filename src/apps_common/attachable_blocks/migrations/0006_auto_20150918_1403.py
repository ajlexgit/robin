# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20150918_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachablereference',
            options={'verbose_name': 'Attached block', 'verbose_name_plural': 'Attached blocks', 'ordering': ('set_name', 'order')},
        ),
        migrations.AddField(
            model_name='attachablereference',
            name='set_name',
            field=models.CharField(max_length=32, verbose_name='set name', default='default'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attachablereference',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block', 'set_name')]),
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
        migrations.RemoveField(
            model_name='attachablereference',
            name='frame',
        ),
    ]
