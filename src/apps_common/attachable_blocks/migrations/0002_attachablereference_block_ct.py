# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachablereference',
            name='block_ct',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='+'),
        ),
    ]
