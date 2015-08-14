# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0004_auto_20150814_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(verbose_name='block type', editable=False, choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'Slider'), ('portfolio.portfolioblock', 'portfolio blocks')], max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_type',
            field=models.CharField(verbose_name='block type', choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'Slider'), ('portfolio.portfolioblock', 'portfolio blocks')], max_length=255),
            preserve_default=True,
        ),
    ]
