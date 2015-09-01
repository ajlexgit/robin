# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(verbose_name='text', max_length=4096)),
                ('rating', models.IntegerField(default=0, editable=False, verbose_name='rating')),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(default=False, editable=False, verbose_name='deleted')),
                ('visible', models.BooleanField(default=True, editable=False, verbose_name='visible')),
                ('order', models.PositiveIntegerField(default=0, editable=False, verbose_name='order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, editable=False, verbose_name='deleted by', blank=True)),
                ('parent', mptt.fields.TreeForeignKey(null=True, to='comments.Comment', verbose_name='parent comment', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
