# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.core.validators
import ckeditor.fields
import libs.media_storage
import django.utils.timezone
import libs.valute_field.fields
import libs.stdimage.fields
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('is_visible', models.BooleanField(db_index=True, verbose_name='visible', default=False)),
                ('product_count', models.PositiveIntegerField(editable=False, help_text='count of immediate visible products', default=0)),
                ('total_product_count', models.PositiveIntegerField(editable=False, help_text='count of visible products', default=0)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='shop.ShopCategory', verbose_name='parent category', null=True, blank=True, related_name='children')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], verbose_name='status', default=1)),
                ('pay_date', models.DateTimeField(editable=False, null=True, verbose_name='pay date')),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)], editable=False)),
                ('session', models.CharField(editable=False, verbose_name='session', max_length=64)),
                ('date', models.DateTimeField(editable=False, verbose_name='create date')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('serial', models.SlugField(unique=True, help_text='Unique identifier of the product', verbose_name='S/N', max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='photo', min_dimensions=(180, 60), variations={'admin': {'crop': False, 'size': (200, 200)}, 'small': {'crop': False, 'size': (160, 160)}, 'admin_micro': {'size': (60, 60), 'crop': False, 'background': (255, 255, 255, 255)}, 'normal': {'crop': False, 'size': (300, 300)}}, aspects=(), storage=libs.media_storage.MediaStorage('shop/product'), upload_to='')),
                ('photo_crop', models.CharField(editable=False, blank=True, verbose_name='stored_crop', max_length=32)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='immediate_products')),
            ],
            options={
                'verbose_name_plural': 'products',
                'ordering': ('-created',),
                'verbose_name': 'product',
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
