# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_auto_20160824_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='seodata',
            name='noindex',
            field=models.BooleanField(help_text='the text on the page should not be indexed', default=False, verbose_name='noindex'),
        ),
    ]
