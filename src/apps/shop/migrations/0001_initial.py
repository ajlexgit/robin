# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import django.core.validators
import mptt.fields
import ckeditor.fields
import libs.stdimage.fields
import django.utils.timezone
import libs.valute_field.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('is_visible', models.BooleanField(db_index=True, verbose_name='visible', default=False)),
                ('product_count', models.PositiveIntegerField(help_text='count of immediate visible products', editable=False, default=0)),
                ('total_product_count', models.PositiveIntegerField(help_text='count of visible products', editable=False, default=0)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, blank=True, verbose_name='parent category', related_name='children', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], verbose_name='status', default=1)),
                ('pay_date', models.DateTimeField(null=True, verbose_name='pay date', editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)], editable=False)),
                ('session', models.CharField(max_length=64, verbose_name='session', editable=False)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('serial', models.SlugField(unique=True, max_length=64, verbose_name='serial number', help_text='Unique identifier of the product')),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), aspects=(), verbose_name='photo', variations={'normal': {'crop': False, 'size': (300, 300)}, 'admin': {'crop': False, 'size': (200, 200)}, 'admin_micro': {'crop': False, 'background': (255, 255, 255, 255), 'size': (60, 60)}, 'small': {'crop': False, 'size': (160, 160)}}, upload_to='', min_dimensions=(180, 60))),
                ('photo_crop', models.CharField(max_length=32, blank=True, verbose_name='stored_crop', editable=False)),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(verbose_name='category', related_name='immediate_products', to='shop.ShopCategory')),
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
            field=models.ForeignKey(to='shop.ShopProduct', verbose_name='product'),
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
