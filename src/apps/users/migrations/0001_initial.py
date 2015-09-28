# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import django.core.validators
import django.utils.timezone
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', libs.stdimage.fields.StdImageField(blank=True, min_dimensions=(150, 150), storage=libs.media_storage.MediaStorage('users/avatar'), upload_to='', verbose_name='avatar', variations={'micro': {'size': (32, 32)}, 'small': {'size': (50, 50)}, 'normal': {'size': (150, 150)}}, aspects='normal')),
                ('avatar_crop', models.CharField(blank=True, verbose_name='stored_crop', editable=False, max_length=32)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
