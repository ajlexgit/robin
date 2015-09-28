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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(verbose_name='text', max_length=4096)),
                ('rating', models.IntegerField(default=0, verbose_name='rating', editable=False)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted', editable=False)),
                ('visible', models.BooleanField(default=True, verbose_name='visible', editable=False)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order', editable=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, editable=False, null=True, verbose_name='deleted by', related_name='+')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='comments.Comment', null=True, verbose_name='parent comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author', related_name='comments')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit', 'Can edit comment'), ('can_delete', 'Can delete comment'), ('can_vote', 'Can vote for comment')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('value', models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')])),
                ('comment', models.ForeignKey(to='comments.Comment', related_name='votes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comment_votes')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='commentvote',
            unique_together=set([('comment', 'user')]),
        ),
    ]
