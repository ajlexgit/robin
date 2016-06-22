# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('network', models.CharField(verbose_name='social network', default='facebook', max_length=32, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')])),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(verbose_name='sheduled for sharing', default=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True, editable=False)),
                ('created', models.DateTimeField(verbose_name='created on', default=django.utils.timezone.now, editable=False)),
                ('posted', models.DateTimeField(verbose_name='posted on', null=True, editable=False)),
                ('content_type', models.ForeignKey(editable=False, null=True, blank=True, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'feed post',
                'verbose_name_plural': 'feeds',
                'ordering': ('-scheduled', '-created'),
            },
        ),
        migrations.AlterIndexTogether(
            name='feedpost',
            index_together=set([('network', 'content_type', 'object_id')]),
        ),
    ]
