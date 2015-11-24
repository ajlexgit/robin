# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, auto_created=True, to='attachable_blocks.AttachableBlock', parent_link=True, primary_key=True)),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'My blocks',
                'verbose_name': 'My block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
