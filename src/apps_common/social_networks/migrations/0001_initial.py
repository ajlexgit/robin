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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(max_length=32, default='facebook', verbose_name='social network', choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')])),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(default=True, verbose_name='sheduled to share')),
                ('object_id', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
                ('posted', models.DateTimeField(editable=False, null=True, verbose_name='posted on')),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', editable=False, null=True)),
            ],
            options={
                'ordering': ('-scheduled', '-created'),
                'verbose_name_plural': 'feeds',
                'verbose_name': 'feed post',
            },
        ),
        migrations.CreateModel(
            name='SocialConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_apikey', models.CharField(blank=True, max_length=48, default='AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg', verbose_name='API Key')),
                ('twitter_client_id', models.CharField(blank=True, max_length=48, verbose_name='API Key')),
                ('twitter_client_secret', models.CharField(blank=True, max_length=64, verbose_name='API Secret')),
                ('twitter_access_token', models.CharField(blank=True, max_length=64, verbose_name='Access Token')),
                ('twitter_access_token_secret', models.CharField(blank=True, max_length=64, verbose_name='Access Token Secret')),
                ('facebook_client_id', models.CharField(blank=True, max_length=48, verbose_name='App ID')),
                ('facebook_client_secret', models.CharField(blank=True, max_length=64, verbose_name='App Secret')),
                ('facebook_access_token', models.TextField(blank=True, verbose_name='Access Token')),
                ('linkedin_client_id', models.CharField(blank=True, max_length=48, verbose_name='API Key')),
                ('linkedin_client_secret', models.CharField(blank=True, max_length=48, verbose_name='API Secret')),
                ('linkedin_access_token', models.TextField(blank=True, verbose_name='Access Token')),
                ('instagram_client_id', models.CharField(blank=True, max_length=48, verbose_name='Client ID')),
                ('instagram_client_secret', models.CharField(blank=True, max_length=48, verbose_name='Client Secret')),
                ('instagram_access_token', models.CharField(blank=True, max_length=64, verbose_name='Access Token')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_google', models.URLField(blank=True, max_length=255, verbose_name='google plus')),
                ('social_twitter', models.URLField(blank=True, max_length=255, verbose_name='twitter')),
                ('social_facebook', models.URLField(blank=True, max_length=255, verbose_name='facebook')),
                ('social_instagram', models.URLField(blank=True, max_length=255, verbose_name='instagram')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
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
