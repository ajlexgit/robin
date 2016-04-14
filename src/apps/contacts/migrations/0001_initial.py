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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(max_length=255, verbose_name='address', blank=True)),
                ('phones', models.CharField(max_length=255, verbose_name='phones', blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords', help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
            ],
            options={
                'verbose_name_plural': 'addresses',
                'verbose_name': 'address',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(max_length=32, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail', blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=2048)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date sent', editable=False)),
                ('referer', models.CharField(max_length=255, blank=True, verbose_name='from page', editable=False)),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='NotifyReciever',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(related_name='recievers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name_plural': 'notify recievers',
                'verbose_name': 'notify reciever',
            },
        ),
    ]
