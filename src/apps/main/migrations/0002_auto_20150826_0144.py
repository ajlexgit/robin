# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientinlineformmodel',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='clientinlineformmodel',
            name='order',
            field=models.PositiveIntegerField(verbose_name='order', editable=False, default=0),
            preserve_default=True,
        ),
    ]
