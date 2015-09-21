# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(150, 150), verbose_name='avatar', aspects='normal', variations={'normal': {'size': (150, 150)}, 'micro': {'size': (32, 32)}, 'small': {'size': (50, 50)}}, blank=True, storage=libs.media_storage.MediaStorage('users/avatar'))),
                ('avatar_crop', models.CharField(blank=True, verbose_name='avatar crop coordinates', max_length=32)),
                ('groups', models.ManyToManyField(related_query_name='user', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', verbose_name='user permissions', help_text='Specific permissions for this user.', blank=True, to='auth.Permission', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
