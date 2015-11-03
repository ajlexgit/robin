# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_clientformmodel_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinlineformmodel',
            name='name',
            field=models.CharField(max_length=128, verbose_name='name'),
        ),
    ]
