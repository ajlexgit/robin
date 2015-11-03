# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151103_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinlineformmodel',
            name='name',
            field=models.CharField(default='Test', max_length=128, verbose_name='name'),
        ),
    ]
