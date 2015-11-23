# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('inv_id', models.PositiveIntegerField(blank=True, verbose_name='InvId', null=True)),
                ('step', models.PositiveSmallIntegerField(choices=[(1, 'Result'), (2, 'Success Page'), (3, 'Fail page')], verbose_name='step')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Message'), (2, 'Warning'), (3, 'Success'), (4, 'Error')], verbose_name='status')),
                ('message', models.CharField(max_length=255, verbose_name='message')),
                ('request', models.TextField(verbose_name='request')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'log messages',
                'verbose_name': 'log message',
                'ordering': ('-created',),
            },
        ),
    ]
