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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255, blank=True)),
                ('phones', models.CharField(verbose_name='phones', max_length=255, blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True, help_text='Double click on the map places marker')),
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
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, serialize=False, to='attachable_blocks.AttachableBlock')),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(verbose_name='phone', max_length=32, blank=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254, blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=1536)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date', editable=False)),
                ('referer', models.CharField(verbose_name='from page', max_length=255, blank=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='MessageReciever',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(to='contacts.ContactsConfig', related_name='recievers')),
            ],
            options={
                'verbose_name_plural': 'message recievers',
                'verbose_name': 'message reciever',
            },
        ),
    ]
