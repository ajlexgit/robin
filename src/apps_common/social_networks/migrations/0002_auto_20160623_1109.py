# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('social_facebook', models.URLField(max_length=255, blank=True, verbose_name='facebook')),
                ('social_twitter', models.URLField(max_length=255, blank=True, verbose_name='twitter')),
                ('social_google', models.URLField(max_length=255, blank=True, verbose_name='google plus')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Links',
            },
        ),
        migrations.AlterField(
            model_name='feedpost',
            name='scheduled',
            field=models.BooleanField(default=True, verbose_name='sheduled to share'),
        ),
    ]
