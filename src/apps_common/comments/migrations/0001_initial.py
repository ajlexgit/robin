# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=4096, verbose_name='text')),
                ('rating', models.IntegerField(verbose_name='rating', editable=False, default=0)),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(verbose_name='deleted', editable=False, default=False)),
                ('visible', models.BooleanField(verbose_name='visible', editable=False, default=True)),
                ('order', models.PositiveIntegerField(verbose_name='order', editable=False, default=0)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(editable=False, null=True, related_name='+', to=settings.AUTH_USER_MODEL, blank=True, verbose_name='deleted by')),
                ('parent', mptt.fields.TreeForeignKey(null=True, to='comments.Comment', blank=True, verbose_name='parent comment')),
                ('user', models.ForeignKey(editable=False, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField()),
                ('comment', models.ForeignKey(related_name='votes', to='comments.Comment')),
                ('user', models.ForeignKey(related_name='comment_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'votes',
                'verbose_name': 'vote',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=set([('comment', 'user')]),
        ),
    ]
