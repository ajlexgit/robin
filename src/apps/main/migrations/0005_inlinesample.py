# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mainpageconfig_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color')),
                ('config', models.ForeignKey(to='main.MainPageConfig', verbose_name='config')),
            ],
            options={
                'verbose_name': 'Inline sample',
                'verbose_name_plural': 'Inline samples',
            },
            bases=(models.Model,),
        ),
    ]
