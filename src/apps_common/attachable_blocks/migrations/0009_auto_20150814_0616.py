# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0008_auto_20150814_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(max_length=255, choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('contacts.contactsblock', 'Contact'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'PhotoSlider'), ('portfolio.portfolioblock', 'Portfolio')], editable=False, verbose_name='block type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_type',
            field=models.CharField(max_length=255, choices=[('blocks.advantagesblock', 'Advantages'), ('blocks.blogblock', 'Blog'), ('contacts.contactsblock', 'Contact'), ('blocks.counterblock', 'Counter'), ('blocks.expertblock', 'Expert'), ('blocks.sliderblock', 'PhotoSlider'), ('portfolio.portfolioblock', 'Portfolio')], verbose_name='block type'),
            preserve_default=True,
        ),
    ]
