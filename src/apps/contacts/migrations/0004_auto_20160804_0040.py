# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20160722_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(verbose_name='number', blank=True, max_length=255)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
            ],
            options={
                'verbose_name': 'phone',
                'verbose_name_plural': 'phones',
                'ordering': ('sort_order',),
            },
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone',
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='address',
            field=models.ForeignKey(related_name='+', to='contacts.Address'),
        ),
    ]
