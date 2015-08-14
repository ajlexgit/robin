# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20150814_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(verbose_name='block type', editable=False, max_length=255, choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'PhotoSlider'), ('portfolio.portfolioblock', 'Portfolio')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_type',
            field=models.CharField(verbose_name='block type', max_length=255, choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'PhotoSlider'), ('portfolio.portfolioblock', 'Portfolio')]),
            preserve_default=True,
        ),
    ]
