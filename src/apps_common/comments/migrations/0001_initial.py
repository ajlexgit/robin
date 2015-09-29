# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(verbose_name='text', max_length=4096)),
                ('rating', models.IntegerField(verbose_name='rating', editable=False, default=0)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False)),
                ('deleted', models.BooleanField(verbose_name='deleted', editable=False, default=False)),
                ('visible', models.BooleanField(verbose_name='visible', editable=False, default=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order', editable=False, default=0)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(verbose_name='deleted by', related_name='+', to=settings.AUTH_USER_MODEL, blank=True, null=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='parent comment', to='comments.Comment', blank=True, null=True)),
                ('user', models.ForeignKey(verbose_name='author', related_name='comments', to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
                'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit', 'Can edit comment'), ('can_delete', 'Can delete comment'), ('can_vote', 'Can vote for comment')),
            },
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('value', models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')])),
                ('comment', models.ForeignKey(to='comments.Comment', related_name='votes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comment_votes')),
            ],
            options={
                'verbose_name_plural': 'votes',
                'verbose_name': 'vote',
            },
        ),
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=set([('comment', 'user')]),
        ),
    ]
