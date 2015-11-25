# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_post_publication_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name_plural': 'posts', 'ordering': ('-publication_date',), 'verbose_name': 'post'},
        ),
    ]
