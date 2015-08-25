# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('position', models.CharField(max_length=12, choices=[('head', 'Head'), ('body_top', 'Body Top'), ('body_bottom', 'Body Bottom')], verbose_name='position')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='site keywords')),
                ('description', models.TextField(blank=True, max_length=160, verbose_name='site description')),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='keywords')),
                ('description', models.TextField(blank=True, max_length=160, verbose_name='description')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'SEO data',
                'verbose_name': 'SEO data',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
