# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, to='attachable_blocks.AttachableBlock', serialize=False, primary_key=True, parent_link=True)),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': 'sample block',
                'verbose_name_plural': 'sample blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
