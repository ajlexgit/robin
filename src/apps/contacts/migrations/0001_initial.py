# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(verbose_name='phone', blank=True, max_length=32)),
                ('email', models.EmailField(verbose_name='e-mail', blank=True, max_length=254)),
                ('message', models.TextField(verbose_name='message', max_length=1536)),
                ('date', models.DateTimeField(verbose_name='date', editable=False, default=django.utils.timezone.now)),
                ('referer', models.CharField(verbose_name='referer', editable=False, blank=True, max_length=255)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(to='contacts.ContactsConfig', related_name='recievers')),
            ],
            options={
                'verbose_name': 'message reciever',
                'verbose_name_plural': 'message recievers',
            },
        ),
    ]
