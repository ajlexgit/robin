# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('old_path', models.CharField(help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, unique=True, verbose_name='redirect from')),
                ('new_path', models.CharField(max_length=200, help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", blank=True, verbose_name='redirect to')),
                ('permanent', models.BooleanField(default=True, verbose_name='permanent')),
                ('created', models.DateField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
            ],
            options={
                'verbose_name_plural': 'redirects',
                'verbose_name': 'redirect',
                'ordering': ('old_path',),
            },
        ),
    ]
