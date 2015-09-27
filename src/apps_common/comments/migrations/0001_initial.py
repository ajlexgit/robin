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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=4096, verbose_name='text')),
                ('rating', models.IntegerField(editable=False, default=0, verbose_name='rating')),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(editable=False, default=False, verbose_name='deleted')),
                ('visible', models.BooleanField(editable=False, default=True, verbose_name='visible')),
                ('sort_order', models.PositiveIntegerField(editable=False, default=0, verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(related_name='+', blank=True, null=True, editable=False, verbose_name='deleted by', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, verbose_name='parent comment', to='comments.Comment')),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('value', models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')])),
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
