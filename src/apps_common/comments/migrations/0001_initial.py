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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=4096, verbose_name='text')),
                ('rating', models.IntegerField(editable=False, verbose_name='rating', default=0)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False)),
                ('deleted', models.BooleanField(editable=False, verbose_name='deleted', default=False)),
                ('visible', models.BooleanField(editable=False, verbose_name='visible', default=True)),
                ('sort_order', models.PositiveIntegerField(editable=False, verbose_name='sort order', default=0)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, verbose_name='deleted by', related_name='+', to=settings.AUTH_USER_MODEL, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, blank=True, verbose_name='parent comment', to='comments.Comment')),
                ('user', models.ForeignKey(verbose_name='author', related_name='comments', to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'verbose_name_plural': 'comments',
                'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit', 'Can edit comment'), ('can_delete', 'Can delete comment'), ('can_vote', 'Can vote for comment')),
                'verbose_name': 'comment',
            },
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
