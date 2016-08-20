# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='posttag',
            name='post',
        ),
        migrations.RemoveField(
            model_name='posttag',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='tags',
        ),
        migrations.DeleteModel(
            name='PostTag',
        ),
    ]
