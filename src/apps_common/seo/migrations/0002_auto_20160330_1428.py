# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(verbose_name='text')),
            ],
            options={
                'verbose_name': 'file',
                'default_permissions': (),
                'verbose_name_plural': 'robots.txt',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='seoconfig',
            options={'verbose_name': 'Default settings'},
        ),
    ]
