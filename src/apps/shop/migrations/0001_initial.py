# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import mptt.fields
import django.utils.timezone
import libs.autoslug
import libs.media_storage
import libs.stdimage.fields
import libs.valute_field.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', unique=True, populate_from=('title',))),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False, db_index=True)),
                ('product_count', models.PositiveIntegerField(editable=False, default=0, help_text='count of immediate visible products')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='shop.ShopCategory', verbose_name='parent category', related_name='children', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], default=1, verbose_name='status')),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', editable=False, validators=[django.core.validators.MinValueValidator(0)])),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', unique=True, populate_from=('title',))),
                ('serial', models.SlugField(verbose_name='S/N', max_length=64, help_text='Unique identifier of the product', unique=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='photo', aspects=(), storage=libs.media_storage.MediaStorage('shop/product'), upload_to='', variations={'small': {'crop': False, 'size': (160, 160)}, 'normal': {'crop': False, 'size': (300, 300)}, 'admin_micro': {'background': (255, 255, 255, 255), 'crop': False, 'size': (60, 60)}, 'admin': {'crop': False, 'size': (200, 200)}}, min_dimensions=(180, 60))),
                ('photo_crop', models.CharField(verbose_name='stored_crop', editable=False, blank=True, max_length=32)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='immediate_products')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(to='shop.ShopOrder', verbose_name='order', related_name='order_products'),
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
