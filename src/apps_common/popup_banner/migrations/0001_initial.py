# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.stdimage.fields
import libs.storages.media_storage
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(help_text='for inner use', max_length=255, verbose_name='label')),
                ('url', models.URLField(verbose_name='url')),
                ('image', libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('popup_banner/image'), verbose_name='image', aspects=('normal',), variations={'admin': {'size': (200, 200)}, 'normal': {'size': (480, 480)}}, upload_to='', min_dimensions=(300, 300))),
                ('header', models.CharField(max_length=255, verbose_name='header', blank=True)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text', blank=True)),
                ('timeout', models.IntegerField(help_text='seconds from page load', verbose_name='timeout', default=10)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=True)),
                ('show_type', models.CharField(max_length=16, verbose_name='show', default='session', choices=[('always', 'Always'), ('session', 'Once per session'), ('once', 'Once per user')])),
                ('since_date', models.DateField(verbose_name='since', default=django.utils.timezone.now)),
                ('to_date', models.DateField(verbose_name='to', null=True, blank=True)),
            ],
            options={
                'ordering': ('-since_date',),
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
            },
        ),
        migrations.CreateModel(
            name='PageAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('regex', models.CharField(max_length=255, verbose_name='URL Regex')),
                ('banner', models.ForeignKey(to='popup_banner.Banner', related_name='pages')),
            ],
            options={
                'ordering': ('regex',),
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
    ]
