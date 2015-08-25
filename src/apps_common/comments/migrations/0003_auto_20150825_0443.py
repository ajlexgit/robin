# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20150825_0302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment')), 'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
    ]
