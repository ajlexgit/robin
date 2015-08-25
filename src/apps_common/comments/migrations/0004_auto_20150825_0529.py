# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20150825_0443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit_post', 'Can edit post comment')), 'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
    ]
