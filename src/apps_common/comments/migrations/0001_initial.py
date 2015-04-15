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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField(verbose_name='text', max_length=4096)),
                ('rating', models.IntegerField(editable=False, default=0, verbose_name='rating')),
                ('created', models.DateTimeField(editable=False, verbose_name='created on')),
                ('deleted', models.BooleanField(editable=False, verbose_name='deleted', default=False)),
                ('visible', models.BooleanField(editable=False, verbose_name='visible', default=True)),
                ('order', models.PositiveIntegerField(editable=False, default=0, verbose_name='order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleted_by', models.ForeignKey(related_name='+', blank=True, null=True, editable=False, verbose_name='deleted by', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, verbose_name='parent comment', to='comments.Comment')),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
