# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hits',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=64, default='undefined', verbose_name='type')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='hits')),
                ('date', models.DateField(verbose_name='date')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='hits',
            unique_together=set([('content_type', 'object_id', 'type', 'date')]),
        ),
    ]
