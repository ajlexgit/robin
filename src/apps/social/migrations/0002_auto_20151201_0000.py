# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUsBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, to='attachable_blocks.AttachableBlock', auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'Blocks "Follow us"',
                'verbose_name': 'Block "Follow us"',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.AlterModelOptions(
            name='socialconfig',
            options={'verbose_name': 'Settings'},
        ),
    ]
