# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0002_subscriber_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Queued'), (10, 'Published')]),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (10, 'Queued'), (20, 'Published'), (21, 'Content setted'), (22, 'Running'), (30, 'Done')]),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Queued'), (10, 'Subscribed'), (20, 'Unsubscribed')]),
        ),
    ]
