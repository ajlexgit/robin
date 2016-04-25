# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20160425_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('config', models.ForeignKey(to='contacts.ContactsConfig', related_name='receivers')),
            ],
            options={
                'verbose_name_plural': 'notify receivers',
                'verbose_name': 'notify receiver',
            },
        ),
        migrations.RemoveField(
            model_name='notifyreciever',
            name='config',
        ),
        migrations.DeleteModel(
            name='NotifyReciever',
        ),
    ]
