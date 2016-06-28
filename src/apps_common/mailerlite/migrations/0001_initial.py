# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.color_field.fields
import ckeditor.fields
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('subject', models.CharField(verbose_name='subject', max_length=255)),
                ('preheader', models.CharField(verbose_name='pre-header', max_length=255, blank=True)),
                ('header_image', libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), verbose_name='preview', upload_to='', variations={'normal': {'quality': 95, 'size': (640, 150)}, 'admin': {'size': (480, 90)}}, aspects='normal', min_dimensions=(640, 150), blank=True)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(editable=False, verbose_name='sent emails', default=0)),
                ('opened', models.PositiveIntegerField(editable=False, verbose_name='opened emails', default=0)),
                ('clicked', models.PositiveIntegerField(editable=False, verbose_name='clicks from emails', default=0)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Draft'), (10, 'Queued'), (20, 'Published'), (21, 'Content setted'), (22, 'Running'), (30, 'Done')], default=0)),
                ('remote_id', models.PositiveIntegerField(editable=False, verbose_name='ID in Mailerlite', db_index=True, default=0)),
                ('remote_mail_id', models.PositiveIntegerField(editable=False, verbose_name='ID in Mailerlite', db_index=True, default=0)),
                ('date_created', models.DateTimeField(editable=False, verbose_name='date created', default=django.utils.timezone.now)),
                ('date_started', models.DateTimeField(editable=False, verbose_name='date started', null=True)),
                ('date_done', models.DateTimeField(editable=False, verbose_name='date done', null=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'campaign',
                'verbose_name_plural': 'campaigns',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('total', models.PositiveIntegerField(editable=False, verbose_name='total subscribers', default=0)),
                ('active', models.PositiveIntegerField(editable=False, verbose_name='active subscribers', default=0)),
                ('unsubscribed', models.PositiveIntegerField(editable=False, verbose_name='unsubscribed', default=0)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Queued'), (10, 'Published')], default=0)),
                ('sent', models.PositiveIntegerField(editable=False, verbose_name='sent emails', default=0)),
                ('opened', models.PositiveIntegerField(editable=False, verbose_name='opened emails', default=0)),
                ('clicked', models.PositiveIntegerField(editable=False, verbose_name='clicks from emails', default=0)),
                ('remote_id', models.PositiveIntegerField(editable=False, verbose_name='ID in Mailerlite', db_index=True, default=0)),
                ('date_created', models.DateTimeField(editable=False, verbose_name='date created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='date updated', auto_now=True)),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('from_email', models.EmailField(verbose_name='sender email', help_text='should be real address', max_length=254, default='manager@example.com')),
                ('from_name', models.CharField(verbose_name='sender name', help_text='should be real name', max_length=255, default='John Smith')),
                ('bg_color', libs.color_field.fields.ColorField(verbose_name='background color', default='#BDC3C7', blank=True)),
                ('bg_image', models.ImageField(storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), verbose_name='background image', upload_to='', blank=True)),
                ('company', models.CharField(verbose_name='company', max_length=255, default='Example')),
                ('website', models.CharField(verbose_name='website address', max_length=255, default='example.com')),
                ('contact_email', models.EmailField(verbose_name='contact email', max_length=254, default='admin@example.com')),
                ('import_groups_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('import_campaigns_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('import_subscribers_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('export_groups_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('export_campaigns_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('export_subscribers_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.EmailField(unique=True, verbose_name='email', max_length=254)),
                ('name', models.CharField(verbose_name='first name', max_length=255, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=255, blank=True)),
                ('company', models.CharField(verbose_name='company', max_length=255, blank=True)),
                ('status', models.SmallIntegerField(verbose_name='status', choices=[(0, 'Queued'), (10, 'Subscribed'), (20, 'Unsubscribed')], default=0)),
                ('sent', models.PositiveIntegerField(editable=False, verbose_name='sent emails', default=0)),
                ('opened', models.PositiveIntegerField(editable=False, verbose_name='opened emails', default=0)),
                ('clicked', models.PositiveIntegerField(editable=False, verbose_name='clicks from emails', default=0)),
                ('remote_id', models.PositiveIntegerField(editable=False, verbose_name='ID in Mailerlite', db_index=True, default=0)),
                ('date_created', models.DateField(editable=False, verbose_name='date subscribed', default=django.utils.timezone.now)),
                ('date_unsubscribe', models.DateField(editable=False, verbose_name='date unsubscribed', null=True)),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'subscriber',
                'verbose_name_plural': 'subscribers',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(to='mailerlite.Group'),
        ),
    ]
