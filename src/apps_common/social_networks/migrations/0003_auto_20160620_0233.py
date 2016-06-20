# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0002_auto_20160615_0244'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SocialPost',
            new_name='FeedPost',
        )
    ]
