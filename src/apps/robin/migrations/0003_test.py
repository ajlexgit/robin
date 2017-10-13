# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robin', '0002_auto_20171010_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('thirdname', models.CharField(max_length=128, verbose_name='thirdname')),
                ('nua', models.CharField(max_length=128, verbose_name='nua')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('sort_order', models.PositiveIntegerField(verbose_name='order', default=0)),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Subscribe',
                'default_permissions': ('change',),
            },
        ),
    ]
