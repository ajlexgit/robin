# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=4096, verbose_name='text')),
                ('rating', models.IntegerField(editable=False, default=0, verbose_name='rating')),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(editable=False, default=False, verbose_name='deleted')),
                ('visible', models.BooleanField(editable=False, default=True, verbose_name='visible')),
                ('order', models.PositiveIntegerField(editable=False, default=0, verbose_name='order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, editable=False, null=True, verbose_name='deleted by')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='comments.Comment', null=True, verbose_name='parent comment')),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author')),
            ],
            options={
                'permissions': (('can_reply', 'Can reply on comment'), ('can_post', 'Can post comment'), ('can_edit', 'Can edit comment'), ('can_delete', 'Can delete comment'), ('can_vote', 'Can vote for comment')),
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
