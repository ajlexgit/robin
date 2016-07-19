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
                ('network', models.CharField(verbose_name='social network', choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], max_length=32, default='facebook')),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(verbose_name='sheduled to share', default=True)),
                ('object_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False, default=django.utils.timezone.now)),
                ('posted', models.DateTimeField(verbose_name='posted on', editable=False, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType', editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('social_facebook', models.URLField(verbose_name='facebook', max_length=255, blank=True)),
                ('social_twitter', models.URLField(verbose_name='twitter', max_length=255, blank=True)),
                ('social_google', models.URLField(verbose_name='google plus', max_length=255, blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
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
