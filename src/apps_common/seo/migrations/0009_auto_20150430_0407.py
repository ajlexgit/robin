# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0008_auto_20150430_0340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seodata',
            options={'verbose_name': 'SEO data', 'verbose_name_plural': 'SEO data'},
        ),
    ]
