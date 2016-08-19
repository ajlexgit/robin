# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import google_maps.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('region', models.CharField(max_length=64, blank=True, verbose_name='region')),
                ('zip', models.CharField(max_length=32, blank=True, verbose_name='zip')),
                ('coords', google_maps.fields.GoogleCoordsField(help_text='Double click on the map places marker', blank=True, verbose_name='coords')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
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
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock')),
                ('header', models.CharField(max_length=128, blank=True, verbose_name='header')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(max_length=32, blank=True, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='e-mail')),
                ('message', models.TextField(max_length=2048, verbose_name='message')),
                ('date', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='date sent')),
                ('referer', models.CharField(max_length=255, editable=False, blank=True, verbose_name='from page')),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name_plural': 'messages',
                'default_permissions': ('delete',),
                'verbose_name': 'message',
            },
        ),
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='receivers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name_plural': 'notify receivers',
                'verbose_name': 'notify receiver',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, blank=True, verbose_name='number')),
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
