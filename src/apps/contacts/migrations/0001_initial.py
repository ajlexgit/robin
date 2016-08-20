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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255)),
                ('region', models.CharField(verbose_name='region', blank=True, max_length=64)),
                ('zip', models.CharField(verbose_name='zip', blank=True, max_length=32)),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True, help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
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
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, serialize=False, to='attachable_blocks.AttachableBlock', auto_created=True, primary_key=True)),
                ('header', models.CharField(verbose_name='header', blank=True, max_length=128)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(verbose_name='phone', blank=True, max_length=32)),
                ('email', models.EmailField(verbose_name='e-mail', blank=True, max_length=254)),
                ('message', models.TextField(verbose_name='message', max_length=2048)),
                ('date', models.DateTimeField(editable=False, verbose_name='date sent', default=django.utils.timezone.now)),
                ('referer', models.CharField(editable=False, verbose_name='from page', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'message',
                'ordering': ('-date',),
                'verbose_name_plural': 'messages',
                'default_permissions': ('delete',),
            },
        ),
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('number', models.CharField(verbose_name='number', blank=True, max_length=255)),
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
