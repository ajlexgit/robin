# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import libs.stdimage.fields
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', max_length=30)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(150, 150), variations={'normal': {'size': (150, 150)}, 'micro': {'size': (32, 32)}, 'small': {'size': (50, 50)}}, blank=True, verbose_name='avatar', storage=libs.media_storage.MediaStorage('users/avatar'), aspects='normal')),
                ('avatar_crop', models.CharField(verbose_name='avatar crop coordinates', max_length=32, blank=True)),
                ('groups', models.ManyToManyField(related_name='user_set', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(related_name='user_set', to='auth.Permission', help_text='Specific permissions for this user.', related_query_name='user', verbose_name='user permissions', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
