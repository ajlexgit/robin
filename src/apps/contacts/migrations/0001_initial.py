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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255, blank=True)),
                ('phones', models.CharField(verbose_name='phones', max_length=255, blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True, help_text='Double click on the map places marker')),
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
                ('attachableblock_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(verbose_name='phone', max_length=32, blank=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254, blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=2048)),
                ('date', models.DateTimeField(verbose_name='date sent', editable=False, default=django.utils.timezone.now)),
                ('referer', models.CharField(verbose_name='from page', blank=True, max_length=255, editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(to='contacts.ContactsConfig', related_name='receivers')),
            ],
            options={
                'verbose_name': 'notify receiver',
                'verbose_name_plural': 'notify receivers',
            },
        ),
    ]
