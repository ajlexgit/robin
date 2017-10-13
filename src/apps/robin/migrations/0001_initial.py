# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RobinPageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_in_school', models.CharField(max_length=2, default='FR', choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')])),
            ],
        ),
        migrations.CreateModel(
            name='Subscribes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('thirdname', models.CharField(max_length=128, verbose_name='thirdname')),
                ('nua', models.CharField(max_length=128, verbose_name='nua')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'ordering': ('sort_order',),
                'default_permissions': ('change',),
                'verbose_name': 'Subscribe',
            },
        ),
    ]
