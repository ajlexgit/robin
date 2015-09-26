# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', unique=True, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=75)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('avatar', libs.stdimage.fields.StdImageField(aspects='normal', blank=True, min_dimensions=(150, 150), verbose_name='avatar', variations={'micro': {'size': (32, 32)}, 'normal': {'size': (150, 150)}, 'small': {'size': (50, 50)}}, storage=libs.media_storage.MediaStorage('users/avatar'), upload_to='')),
                ('avatar_crop', models.CharField(editable=False, verbose_name='stored_crop', blank=True, max_length=32)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', verbose_name='groups', related_name='user_set', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', verbose_name='user permissions', related_name='user_set', to='auth.Permission', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
