# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='total_product_count',
            field=models.PositiveIntegerField(default=0, help_text='count of visible products', editable=False),
        ),
    ]
