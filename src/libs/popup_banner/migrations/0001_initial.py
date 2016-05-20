# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.storages.media_storage
import libs.stdimage.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('label', models.CharField(help_text='for inner use', verbose_name='label', max_length=255)),
                ('timeout', models.IntegerField(help_text='seconds from page load', default=10, verbose_name='timeout')),
                ('since_date', models.DateField(default=django.utils.timezone.now, verbose_name='since')),
                ('to_date', models.DateField(verbose_name='to', null=True, blank=True)),
                ('url', models.URLField(verbose_name='url')),
                ('image', libs.stdimage.fields.StdImageField(aspects=('normal',), min_dimensions=(300, 300), storage=libs.storages.media_storage.MediaStorage('popup_banner/image'), upload_to='', verbose_name='image', variations={'admin': {'size': (200, 200)}, 'normal': {'size': (480, 480)}})),
                ('header', models.CharField(max_length=255, verbose_name='header', blank=True)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text', blank=True)),
                ('button_text', models.CharField(max_length=48, verbose_name='button text', blank=True)),
                ('is_visible', models.BooleanField(default=True, verbose_name='visible')),
                ('show_type', models.CharField(choices=[('always', 'Always'), ('session', 'Once per session'), ('once', 'Once per user')], default='session', verbose_name='show', max_length=16)),
            ],
            options={
                'verbose_name_plural': 'banners',
                'verbose_name': 'banner',
                'ordering': ('-since_date',),
            },
        ),
        migrations.CreateModel(
            name='PageAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('regex', models.CharField(verbose_name='URL Regex', max_length=255)),
                ('banner', models.ForeignKey(related_name='pages', to='popup_banner.Banner')),
            ],
            options={
                'verbose_name_plural': 'pages',
                'verbose_name': 'page',
                'ordering': ('regex',),
            },
        ),
    ]
