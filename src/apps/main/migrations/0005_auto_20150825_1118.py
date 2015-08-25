# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_clientformmodel_clientinlineformmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientformmodel',
            name='title',
            field=models.CharField(blank=True, default='Example', max_length=128, verbose_name='title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientinlineformmodel',
            name='name',
            field=models.CharField(verbose_name='name', default='Test', max_length=128),
            preserve_default=True,
        ),
    ]
