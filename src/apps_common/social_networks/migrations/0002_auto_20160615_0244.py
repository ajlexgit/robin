# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialpost',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', editable=False, null=True),
        ),
        migrations.AddField(
            model_name='socialpost',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='socialpost',
            name='network',
            field=models.CharField(default='facebook', choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], verbose_name='social network', max_length=32),
        ),
        migrations.AlterIndexTogether(
            name='socialpost',
            index_together=set([('network', 'content_type', 'object_id')]),
        ),
    ]
