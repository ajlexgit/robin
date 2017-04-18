# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import django.utils.timezone
import ckeditor.fields
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', default=0, editable=False)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', default=0, editable=False)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', default=0, editable=False)),
                ('status', models.SmallIntegerField(choices=[(0, 'Draft'), (10, 'Queued'), (20, 'Running'), (30, 'Done')], verbose_name='status', default=0)),
                ('published', models.BooleanField(verbose_name='published', default=False)),
                ('remote_id', models.PositiveIntegerField(db_index=True, verbose_name='ID in Mailerlite', default=0, editable=False)),
                ('remote_mail_id', models.PositiveIntegerField(db_index=True, verbose_name='ID in Mailerlite', default=0, editable=False)),
                ('date_created', models.DateTimeField(verbose_name='date created', default=django.utils.timezone.now, editable=False)),
                ('date_started', models.DateTimeField(null=True, verbose_name='date started', editable=False)),
                ('date_done', models.DateTimeField(null=True, verbose_name='date done', editable=False)),
            ],
            options={
                'default_permissions': ('add', 'change'),
                'verbose_name': 'campaign',
                'verbose_name_plural': 'campaigns',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('subscribable', models.BooleanField(verbose_name='subscribable', default=False)),
                ('total', models.PositiveIntegerField(verbose_name='total subscribers', default=0, editable=False)),
                ('active', models.PositiveIntegerField(verbose_name='active subscribers', default=0, editable=False)),
                ('unsubscribed', models.PositiveIntegerField(verbose_name='unsubscribed', default=0, editable=False)),
                ('status', models.SmallIntegerField(choices=[(0, 'Queued'), (10, 'Published')], verbose_name='status', default=0)),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', default=0, editable=False)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', default=0, editable=False)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', default=0, editable=False)),
                ('remote_id', models.PositiveIntegerField(db_index=True, verbose_name='ID in Mailerlite', default=0, editable=False)),
                ('date_created', models.DateTimeField(verbose_name='date created', default=django.utils.timezone.now, editable=False)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'list',
                'verbose_name_plural': 'lists',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('from_email', models.EmailField(max_length=254, verbose_name='e-mail', default='manager@example.com', help_text='must be valid and actually exists')),
                ('from_name', models.CharField(max_length=255, verbose_name='name', default='John Smith', help_text='should be your name')),
                ('bg_color', libs.color_field.fields.ColorField(verbose_name='background color', blank=True, default='#BDC3C7')),
                ('bg_image', models.ImageField(upload_to='', storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), verbose_name='background image', blank=True)),
                ('footer_text', models.TextField(verbose_name='text', blank=True)),
                ('website', models.URLField(max_length=255, verbose_name='website address')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='contact email', default='admin@example.com')),
                ('import_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=255, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='last name', blank=True)),
                ('company', models.CharField(max_length=255, verbose_name='company', blank=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Queued'), (10, 'Subscribed'), (-10, 'Unsubscribed'), (-20, 'Not exists')], verbose_name='status', default=0)),
                ('sent', models.PositiveIntegerField(verbose_name='sent emails', default=0, editable=False)),
                ('opened', models.PositiveIntegerField(verbose_name='opened emails', default=0, editable=False)),
                ('clicked', models.PositiveIntegerField(verbose_name='clicks from emails', default=0, editable=False)),
                ('remote_id', models.PositiveIntegerField(db_index=True, verbose_name='ID in Mailerlite', default=0, editable=False)),
                ('date_created', models.DateField(verbose_name='date subscribed', default=django.utils.timezone.now, editable=False)),
                ('date_unsubscribe', models.DateTimeField(null=True, verbose_name='date unsubscribed', editable=False)),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'default_permissions': ('add', 'change'),
                'verbose_name': 'subscriber',
                'verbose_name_plural': 'subscribers',
                'ordering': ('-date_created', 'id'),
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(verbose_name='lists', to='mailerlite.Group'),
        ),
    ]
