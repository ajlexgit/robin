# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0004_auto_20150506_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='position',
            field=models.CharField(choices=[('head', 'Head'), ('body_top', 'Body Top'), ('body_bottom', 'Body Bottom')], verbose_name='position', max_length=12),
            preserve_default=True,
        ),
    ]
