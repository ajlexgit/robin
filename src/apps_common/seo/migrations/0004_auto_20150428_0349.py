# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0003_auto_20150427_1036'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seotext',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
