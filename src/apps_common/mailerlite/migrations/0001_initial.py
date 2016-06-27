# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.color_field.fields
import libs.stdimage.fields
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('from_email', models.EmailField(max_length=254, help_text='should be real address', verbose_name='sender email', blank=True)),
                ('from_name', models.CharField(max_length=255, help_text='should be real name', verbose_name='sender name', blank=True)),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('header_image', libs.stdimage.fields.StdImageField(min_dimensions=(640, 120), variations={'admin': {'size': (480, 90)}, 'normal': {'size': (640, 120), 'quality': 95}}, upload_to='', aspects='normal', storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), verbose_name='preview', blank=True)),
                ('text', ckeditor.fields.CKEditorField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'Draft'), (1, 'Queued'), (2, 'Running'), (3, 'Done')], verbose_name='status')),
                ('remote_id', models.PositiveIntegerField(default=0, verbose_name='ID in Mailerlite', editable=False, db_index=True)),
                ('remote_mail_id', models.PositiveIntegerField(default=0, verbose_name='ID in Mailerlite', editable=False, db_index=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created', editable=False)),
                ('date_started', models.DateTimeField(verbose_name='date started', editable=False, null=True)),
                ('date_done', models.DateTimeField(verbose_name='date done', editable=False, null=True)),
            ],
            options={
                'verbose_name': 'campaign',
                'verbose_name_plural': 'campaigns',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='total subscribers', editable=False)),
                ('active', models.PositiveIntegerField(default=0, verbose_name='active subscribers', editable=False)),
                ('unsubscribed', models.PositiveIntegerField(default=0, verbose_name='unsubscribed', editable=False)),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('remote_id', models.PositiveIntegerField(default=0, verbose_name='ID in Mailerlite', editable=False, db_index=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created', editable=False)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('from_email', models.EmailField(max_length=254, default='manager@example.com', help_text='should be real address', verbose_name='sender email')),
                ('from_name', models.CharField(max_length=255, default='John Smith', help_text='should be real name', verbose_name='sender name')),
                ('bg_color', libs.color_field.fields.ColorField(default='#BDC3C7', verbose_name='background color', blank=True)),
                ('bg_image', models.ImageField(storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), upload_to='', verbose_name='background image', blank=True)),
                ('company', models.CharField(max_length=255, default='Example', verbose_name='company')),
                ('website', models.CharField(max_length=255, default='example.com', verbose_name='website address')),
                ('contact_email', models.EmailField(max_length=254, default='admin@example.com', verbose_name='contact email')),
                ('import_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email', unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='last name', blank=True)),
                ('company', models.CharField(max_length=255, verbose_name='company', blank=True)),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('remote_id', models.PositiveIntegerField(default=0, verbose_name='ID in Mailerlite', editable=False, db_index=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now, verbose_name='date subscribed', editable=False)),
                ('date_unsubscribe', models.DateField(verbose_name='date unsubscribed', editable=False, null=True)),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'verbose_name': 'subscriber',
                'verbose_name_plural': 'subscribers',
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(to='mailerlite.Group'),
        ),
    ]
