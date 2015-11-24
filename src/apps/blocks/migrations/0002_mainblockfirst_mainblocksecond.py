# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='attachable_blocks.AttachableBlock', primary_key=True)),
            ],
            options={
                'verbose_name': 'First block',
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='attachable_blocks.AttachableBlock', primary_key=True)),
            ],
            options={
                'verbose_name': 'Second block',
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
