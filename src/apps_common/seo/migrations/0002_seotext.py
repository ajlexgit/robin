# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoText',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('url', models.URLField(verbose_name='URL')),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'SEO text',
                'verbose_name_plural': 'SEO texts',
                'ordering': ('url',),
            },
            bases=(models.Model,),
        ),
    ]
