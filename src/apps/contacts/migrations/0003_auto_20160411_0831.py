# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20160330_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyReciever',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(related_name='recievers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name': 'notify reciever',
                'verbose_name_plural': 'notify recievers',
            },
        ),
        migrations.RemoveField(
            model_name='messagereciever',
            name='config',
        ),
        migrations.DeleteModel(
            name='MessageReciever',
        ),
    ]
