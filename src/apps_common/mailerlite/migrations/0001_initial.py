# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.fields
import django.utils.timezone
import libs.color_field.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('subject', models.CharField(verbose_name='subject', max_length=255)),
                ('preheader', models.CharField(verbose_name='pre-header', max_length=255, blank=True)),
                ('header_image', libs.stdimage.fields.StdImageField(verbose_name='preview', blank=True, storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), min_dimensions=(640, 150), aspects='normal', upload_to='', variations={'admin': {'size': (480, 90)}, 'normal': {'quality': 95, 'size': (640, 150)}})),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', editable=False, default=0)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', editable=False, default=0)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', editable=False, default=0)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Draft'), (10, 'Queued'), (20, 'Published'), (21, 'Content setted'), (22, 'Running'), (30, 'Done')], default=0)),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', db_index=True, editable=False, default=0)),
                ('remote_mail_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', db_index=True, editable=False, default=0)),
                ('date_created', models.DateTimeField(verbose_name='date created', editable=False, default=django.utils.timezone.now)),
                ('date_started', models.DateTimeField(verbose_name='date started', null=True, editable=False)),
                ('date_done', models.DateTimeField(verbose_name='date done', null=True, editable=False)),
            ],
            options={
                'verbose_name': 'campaign',
                'ordering': ('-date_created',),
                'verbose_name_plural': 'campaigns',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('total', models.PositiveIntegerField(verbose_name='total subscribers', editable=False, default=0)),
                ('active', models.PositiveIntegerField(verbose_name='active subscribers', editable=False, default=0)),
                ('unsubscribed', models.PositiveIntegerField(verbose_name='unsubscribed', editable=False, default=0)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Queued'), (10, 'Published')], default=0)),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', editable=False, default=0)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', editable=False, default=0)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', editable=False, default=0)),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', db_index=True, editable=False, default=0)),
                ('date_created', models.DateTimeField(verbose_name='date created', editable=False, default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'verbose_name': 'group',
                'ordering': ('-date_created',),
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('from_email', models.EmailField(verbose_name='sender email', max_length=254, help_text='should be real address', default='manager@example.com')),
                ('from_name', models.CharField(verbose_name='sender name', max_length=255, help_text='should be real name', default='John Smith')),
                ('bg_color', libs.color_field.fields.ColorField(verbose_name='background color', blank=True, default='#BDC3C7')),
                ('bg_image', models.ImageField(verbose_name='background image', blank=True, upload_to='', storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'))),
                ('company', models.CharField(verbose_name='company', max_length=255, default='Example')),
                ('website', models.CharField(verbose_name='website address', max_length=255, default='example.com')),
                ('contact_email', models.EmailField(verbose_name='contact email', max_length=254, default='admin@example.com')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('email', models.EmailField(verbose_name='email', max_length=254, unique=True)),
                ('name', models.CharField(verbose_name='first name', max_length=255, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=255, blank=True)),
                ('company', models.CharField(verbose_name='company', max_length=255, blank=True)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Queued'), (10, 'Subscribed'), (20, 'Unsubscribed')], default=0)),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', editable=False, default=0)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', editable=False, default=0)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', editable=False, default=0)),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', db_index=True, editable=False, default=0)),
                ('date_created', models.DateField(verbose_name='date subscribed', editable=False, default=django.utils.timezone.now)),
                ('date_unsubscribe', models.DateField(verbose_name='date unsubscribed', null=True, editable=False)),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'verbose_name': 'subscriber',
                'ordering': ('-date_created',),
                'verbose_name_plural': 'subscribers',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(to='mailerlite.Group'),
        ),
    ]
