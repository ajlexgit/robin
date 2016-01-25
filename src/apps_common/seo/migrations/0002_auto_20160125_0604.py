# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seodata',
            options={'verbose_name_plural': 'SEO data', 'verbose_name': 'SEO data', 'default_permissions': ('change',)},
        ),
    ]
