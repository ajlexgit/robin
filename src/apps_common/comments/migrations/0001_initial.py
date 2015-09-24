# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=4096, verbose_name='text')),
                ('rating', models.IntegerField(editable=False, verbose_name='rating', default=0)),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(editable=False, verbose_name='deleted', default=False)),
                ('visible', models.BooleanField(editable=False, verbose_name='visible', default=True)),
                ('order', models.PositiveIntegerField(editable=False, verbose_name='order', default=0)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', editable=False, null=True, verbose_name='deleted by', blank=True)),
                ('parent', mptt.fields.TreeForeignKey(to='comments.Comment', null=True, verbose_name='parent comment', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='comments', verbose_name='author')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
                'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit', 'Can edit comment'), ('can_delete', 'Can delete comment'), ('can_vote', 'Can vote for comment')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('value', models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')])),
                ('comment', models.ForeignKey(to='comments.Comment', related_name='votes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comment_votes')),
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
