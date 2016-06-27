# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0003_auto_20160627_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='preheader',
            field=models.CharField(verbose_name='pre-header', max_length=255, default=''),
            preserve_default=False,
        ),
    ]
