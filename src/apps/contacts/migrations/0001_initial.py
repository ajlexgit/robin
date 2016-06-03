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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='address')),
                ('phones', models.CharField(blank=True, max_length=255, verbose_name='phones')),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords', help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
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
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='attachable_blocks.AttachableBlock', serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
                ('message', models.TextField(max_length=2048, verbose_name='message')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date sent', editable=False)),
                ('referer', models.CharField(blank=True, max_length=255, verbose_name='from page', editable=False)),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='receivers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name_plural': 'notify receivers',
                'verbose_name': 'notify receiver',
            },
        ),
    ]
