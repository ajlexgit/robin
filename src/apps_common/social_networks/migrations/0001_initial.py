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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('network', models.CharField(verbose_name='social network', default='facebook', choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], max_length=32)),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(verbose_name='sheduled to share', default=True)),
                ('object_id', models.PositiveIntegerField(editable=False, null=True, blank=True)),
                ('created', models.DateTimeField(editable=False, verbose_name='created on', default=django.utils.timezone.now)),
                ('posted', models.DateTimeField(editable=False, null=True, verbose_name='posted on')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', editable=False, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'feed post',
                'ordering': ('-scheduled', '-created'),
                'verbose_name_plural': 'feeds',
            },
        ),
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('social_facebook', models.URLField(verbose_name='facebook', blank=True, max_length=255)),
                ('social_twitter', models.URLField(verbose_name='twitter', blank=True, max_length=255)),
                ('social_google', models.URLField(verbose_name='google plus', blank=True, max_length=255)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Links',
                'default_permissions': ('change',),
            },
        ),
        migrations.AlterIndexTogether(
            name='feedpost',
            index_together=set([('network', 'content_type', 'object_id')]),
        ),
    ]
