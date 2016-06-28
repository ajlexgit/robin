# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import django.utils.timezone
import libs.stdimage.fields
import libs.storages.media_storage
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('preheader', models.CharField(blank=True, max_length=255, verbose_name='pre-header')),
                ('header_image', libs.stdimage.fields.StdImageField(variations={'admin': {'size': (480, 90)}, 'normal': {'size': (640, 150), 'quality': 95}}, min_dimensions=(640, 150), blank=True, verbose_name='preview', storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), upload_to='', aspects='normal')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('status', models.SmallIntegerField(choices=[(0, 'Draft'), (1, 'Queued'), (2, 'Running'), (3, 'Done')], default=0, verbose_name='status')),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', default=0, db_index=True, editable=False)),
                ('remote_mail_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', default=0, db_index=True, editable=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created', editable=False)),
                ('date_started', models.DateTimeField(verbose_name='date started', editable=False, null=True)),
                ('date_done', models.DateTimeField(verbose_name='date done', editable=False, null=True)),
            ],
            options={
                'verbose_name_plural': 'campaigns',
                'verbose_name': 'campaign',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='total subscribers', editable=False)),
                ('active', models.PositiveIntegerField(default=0, verbose_name='active subscribers', editable=False)),
                ('unsubscribed', models.PositiveIntegerField(default=0, verbose_name='unsubscribed', editable=False)),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', default=0, db_index=True, editable=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created', editable=False)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'verbose_name_plural': 'groups',
                'verbose_name': 'group',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('from_email', models.EmailField(help_text='should be real address', default='manager@example.com', max_length=254, verbose_name='sender email')),
                ('from_name', models.CharField(help_text='should be real name', default='John Smith', max_length=255, verbose_name='sender name')),
                ('bg_color', libs.color_field.fields.ColorField(blank=True, default='#BDC3C7', verbose_name='background color')),
                ('bg_image', models.ImageField(blank=True, storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), verbose_name='background image', upload_to='')),
                ('company', models.CharField(default='Example', max_length=255, verbose_name='company')),
                ('website', models.CharField(default='example.com', max_length=255, verbose_name='website address')),
                ('contact_email', models.EmailField(default='admin@example.com', max_length=254, verbose_name='contact email')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(verbose_name='email', max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='last name')),
                ('company', models.CharField(blank=True, max_length=255, verbose_name='company')),
                ('sent', models.PositiveIntegerField(default=0, verbose_name='sent emails', editable=False)),
                ('opened', models.PositiveIntegerField(default=0, verbose_name='opened emails', editable=False)),
                ('clicked', models.PositiveIntegerField(default=0, verbose_name='clicks from emails', editable=False)),
                ('remote_id', models.PositiveIntegerField(verbose_name='ID in Mailerlite', default=0, db_index=True, editable=False)),
                ('date_created', models.DateField(default=django.utils.timezone.now, verbose_name='date subscribed', editable=False)),
                ('date_unsubscribe', models.DateField(verbose_name='date unsubscribed', editable=False, null=True)),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'verbose_name_plural': 'subscribers',
                'verbose_name': 'subscriber',
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(to='mailerlite.Group'),
        ),
    ]
