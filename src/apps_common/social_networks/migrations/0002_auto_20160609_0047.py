# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialpost',
            name='image',
        ),
        migrations.AddField(
            model_name='socialpost',
            name='posted',
            field=models.DateTimeField(verbose_name='posted on', editable=False, null=True),
        ),
    ]
