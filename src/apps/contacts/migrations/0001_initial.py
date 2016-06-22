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
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', help_text='Double click on the map places marker', blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, to='attachable_blocks.AttachableBlock', auto_created=True, primary_key=True, parent_link=True)),
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
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
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
                ('date', models.DateTimeField(verbose_name='date sent', default=django.utils.timezone.now, editable=False)),
                ('referer', models.CharField(verbose_name='from page', blank=True, max_length=255, editable=False)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ('-date',),
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
