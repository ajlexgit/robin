# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Queued'), (1, 'Subscribed'), (2, 'Unsubscribed')], verbose_name='status', default=0),
        ),
    ]
