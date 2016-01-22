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
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('phone', models.CharField(max_length=32, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail', blank=True)),
                ('message', models.TextField(max_length=1536, verbose_name='message')),
                ('date', models.DateTimeField(verbose_name='date', default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='MessageReciever',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='recievers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name': 'message reciever',
                'verbose_name_plural': 'message recievers',
            },
        ),
    ]
