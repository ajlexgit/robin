# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import google_maps.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255)),
                ('region', models.CharField(blank=True, verbose_name='region', max_length=64)),
                ('zip', models.CharField(blank=True, verbose_name='zip', max_length=32)),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords', help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'address',
                'ordering': ('sort_order',),
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(blank=True, verbose_name='header', max_length=128)),
            ],
            options={
                'verbose_name': 'Contact block',
                'verbose_name_plural': 'Contact blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='ContactsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(blank=True, verbose_name='phone', max_length=32)),
                ('email', models.EmailField(blank=True, verbose_name='e-mail', max_length=254)),
                ('message', models.TextField(verbose_name='message', max_length=2048)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date sent', editable=False)),
                ('referer', models.CharField(blank=True, verbose_name='from page', editable=False, max_length=255)),
            ],
            options={
                'default_permissions': ('delete',),
                'verbose_name': 'message',
                'ordering': ('-date',),
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(related_name='receivers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name': 'notify receiver',
                'verbose_name_plural': 'notify receivers',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('number', models.CharField(blank=True, verbose_name='number', max_length=255)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('address', models.ForeignKey(related_name='+', to='contacts.Address')),
            ],
            options={
                'verbose_name': 'phone',
                'ordering': ('sort_order',),
                'verbose_name_plural': 'phones',
            },
        ),
    ]
