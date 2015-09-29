# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.valute_field.fields
import mptt.fields
import libs.stdimage.fields
import django.core.validators
import libs.autoslug
import ckeditor.fields
import django.utils.timezone
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per item')),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', db_index=True, default=False)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='parent category', related_name='children', to='shop.ShopCategory', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(1, 'Not paid'), (2, 'Paid')])),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)], editable=False)),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('serial', models.SlugField(verbose_name='S/N', help_text='Unique identifier of the product', unique=True, max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='photo', variations={'admin_micro': {'background': (255, 255, 255, 255), 'crop': False, 'size': (60, 60)}, 'small': {'crop': False, 'size': (120, 120)}, 'normal': {'crop': False, 'size': (300, 300)}, 'admin': {'crop': False, 'size': (200, 200)}}, storage=libs.media_storage.MediaStorage('shop/product'), min_dimensions=(180, 60), upload_to='', aspects=())),
                ('photo_crop', models.CharField(verbose_name='stored_crop', editable=False, max_length=32, blank=True)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(verbose_name='category', related_name='products', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(verbose_name='order', related_name='order_products', to='shop.ShopOrder'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.ShopProduct'),
        ),
        migrations.AlterIndexTogether(
            name='shopproduct',
            index_together=set([('category', 'is_visible')]),
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set([('order', 'product')]),
        ),
    ]
