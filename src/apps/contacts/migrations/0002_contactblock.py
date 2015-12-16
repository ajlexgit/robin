# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0004_auto_20151214_0959'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True)),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
            ],
            options={
                'verbose_name_plural': 'Contact blocks',
                'verbose_name': 'Contact block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
