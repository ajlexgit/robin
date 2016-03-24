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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='address')),
                ('phones', models.CharField(blank=True, max_length=255, verbose_name='phones')),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, help_text='Double click on the map places marker', verbose_name='coords')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
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
                ('attachableblock_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='attachable_blocks.AttachableBlock')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
                ('message', models.TextField(max_length=2048, verbose_name='message')),
                ('date', models.DateTimeField(editable=False, verbose_name='date', default=django.utils.timezone.now)),
                ('referer', models.CharField(blank=True, verbose_name='from page', max_length=255, editable=False)),
            ],
            options={
                'verbose_name': 'message',
                'ordering': ('-date',),
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='MessageReciever',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='recievers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name_plural': 'message recievers',
                'verbose_name': 'message reciever',
            },
        ),
    ]
