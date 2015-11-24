# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to='attachable_blocks.AttachableBlock', parent_link=True)),
                ('title', models.CharField(verbose_name='title', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Sample block',
                'verbose_name_plural': 'Sample blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
