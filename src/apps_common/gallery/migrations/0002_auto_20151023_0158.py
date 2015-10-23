# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitembase',
            name='created',
            field=models.DateTimeField(verbose_name='created on', blank=True),
        ),
    ]
