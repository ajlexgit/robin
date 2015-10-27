# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import ckeditor.fields
import libs.media_storage
import libs.valute_field.fields
import libs.stdimage.fields
import libs.autoslug
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False, db_index=True)),
                ('product_count', models.PositiveIntegerField(default=0, editable=False, help_text='count of immediate visible products')),
                ('total_product_count', models.PositiveIntegerField(default=0, editable=False, help_text='count of visible products')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, related_name='children', verbose_name='parent category', to='shop.ShopCategory', blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(1, 'Not paid'), (2, 'Paid')])),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='products cost', editable=False)),
                ('session', models.CharField(verbose_name='session', max_length=64, editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('serial', models.SlugField(verbose_name='serial number', help_text='Unique identifier of the product', unique=True, max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), upload_to='', min_dimensions=(180, 60), verbose_name='photo', aspects=(), variations={'normal': {'crop': False, 'size': (300, 300)}, 'admin_micro': {'background': (255, 255, 255, 255), 'crop': False, 'size': (60, 60)}, 'small': {'crop': False, 'size': (160, 160)}, 'admin': {'crop': False, 'size': (200, 200)}})),
                ('photo_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(related_name='immediate_products', verbose_name='category', to='shop.ShopCategory')),
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
            field=models.ForeignKey(related_name='order_products', verbose_name='order', to='shop.ShopOrder'),
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
