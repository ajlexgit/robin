# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import libs.stdimage.fields
import django.contrib.auth.models
import libs.media_storage
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', unique=True, max_length=30, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', libs.stdimage.fields.StdImageField(aspects='normal', min_dimensions=(150, 150), upload_to='', verbose_name='avatar', variations={'micro': {'size': (32, 32)}, 'small': {'size': (50, 50)}, 'normal': {'size': (150, 150)}}, storage=libs.media_storage.MediaStorage('users/avatar'), blank=True)),
                ('avatar_crop', models.CharField(max_length=32, blank=True, verbose_name='stored_crop', editable=False)),
                ('groups', models.ManyToManyField(related_name='user_set', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(related_name='user_set', verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', blank=True)),
            ],
            options={
                'permissions': (('admin_menu', 'Can see hidden menu items'),),
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
