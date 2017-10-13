# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('region', models.CharField(blank=True, max_length=64, verbose_name='region')),
                ('zip', models.CharField(blank=True, max_length=32, verbose_name='zip')),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords', help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name_plural': 'addresses',
                'verbose_name': 'address',
            },
        ),
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock')),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
            ],
            options={
                'verbose_name_plural': 'Contact blocks',
                'verbose_name': 'Contact block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='ContactsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
                ('message', models.TextField(max_length=2048, verbose_name='message')),
                ('date', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='date sent')),
                ('referer', models.CharField(blank=True, max_length=512, verbose_name='from page', editable=False)),
            ],
            options={
                'ordering': ('-date',),
                'default_permissions': ('delete',),
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
            },
        ),
        migrations.CreateModel(
            name='NotificationReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='receivers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name_plural': 'notification receivers',
                'verbose_name': 'notification receiver',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=255, verbose_name='number')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('address', models.ForeignKey(related_name='+', to='contacts.Address')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name_plural': 'phones',
                'verbose_name': 'phone',
            },
        ),
    ]
