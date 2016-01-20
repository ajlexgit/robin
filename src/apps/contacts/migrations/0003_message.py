# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_contactblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(max_length=32, blank=True, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='e-mail')),
                ('message', models.TextField(max_length=1024, verbose_name='message')),
                ('date', models.DateTimeField(editable=False, verbose_name='date')),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
                'ordering': ('-date',),
            },
        ),
    ]
