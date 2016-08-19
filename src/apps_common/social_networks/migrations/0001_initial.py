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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], max_length=32, default='facebook', verbose_name='social network')),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(default=True, verbose_name='sheduled to share')),
                ('object_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
                ('posted', models.DateTimeField(null=True, editable=False, verbose_name='posted on')),
                ('content_type', models.ForeignKey(null=True, editable=False, blank=True, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-scheduled', '-created'),
                'verbose_name_plural': 'feeds',
                'verbose_name': 'feed post',
            },
        ),
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('social_facebook', models.URLField(max_length=255, blank=True, verbose_name='facebook')),
                ('social_twitter', models.URLField(max_length=255, blank=True, verbose_name='twitter')),
                ('social_google', models.URLField(max_length=255, blank=True, verbose_name='google plus')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Links',
            },
        ),
        migrations.AlterIndexTogether(
            name='feedpost',
            index_together=set([('network', 'content_type', 'object_id')]),
        ),
    ]
