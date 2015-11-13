# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20151105_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporder',
            name='status',
        ),
        migrations.AddField(
            model_name='shoporder',
            name='archivation_date',
            field=models.DateTimeField(editable=False, verbose_name='archivation date', null=True),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='cancel_date',
            field=models.DateTimeField(editable=False, verbose_name='cancel date', null=True),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='check_date',
            field=models.DateTimeField(editable=False, verbose_name='check date', null=True),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='confirm_date',
            field=models.DateTimeField(editable=False, verbose_name='confirm date', null=True),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='is_archived',
            field=models.BooleanField(editable=False, default=False, verbose_name='archived'),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='is_cancelled',
            field=models.BooleanField(default=False, verbose_name='cancelled'),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='checked'),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='is_confirmed',
            field=models.BooleanField(editable=False, help_text='Confirmed by the user', default=False, verbose_name='confirmed'),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='paid'),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='uuid',
            field=models.UUIDField(editable=False, unique=True, verbose_name='UUID', default=uuid.uuid4),
        ),
    ]
