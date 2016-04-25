# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifyreciever',
            options={'verbose_name': 'notify receiver', 'verbose_name_plural': 'notify receivers'},
        ),
        migrations.AlterField(
            model_name='notifyreciever',
            name='config',
            field=models.ForeignKey(to='contacts.ContactsConfig', related_name='receivers'),
        ),
    ]
