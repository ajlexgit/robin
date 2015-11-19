# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import project.admin
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('inv_id', models.PositiveIntegerField(null=True, verbose_name='InvId', blank=True)),
                ('step', models.PositiveSmallIntegerField(verbose_name='step', choices=[(1, 'Result'), (2, 'Success Page'), (3, 'Fail page')])),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Message'), (2, 'Warning'), (3, 'Success'), (4, 'Error')])),
                ('message', models.CharField(verbose_name='Message', max_length=255)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'log message',
                'verbose_name_plural': 'log messages',
                'ordering': ('-created',),
            },
            bases=(project.admin.ModelAdminMixin, models.Model),
        ),
    ]
