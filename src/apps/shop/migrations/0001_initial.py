# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import django.core.validators
import libs.autoslug
import mptt.fields
import libs.valute_field.fields
import django.utils.timezone
import libs.media_storage
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('is_visible', models.BooleanField(db_index=True, verbose_name='visible', default=False)),
                ('product_count', models.PositiveIntegerField(editable=False, help_text='count of immediate visible products', default=0)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='shop.ShopCategory', null=True, verbose_name='parent category', related_name='children')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], verbose_name='status', default=1)),
                ('pay_date', models.DateTimeField(editable=False, null=True, verbose_name='pay date')),
                ('products_cost', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], editable=False, verbose_name='products cost')),
                ('session', models.CharField(editable=False, max_length=64, verbose_name='session')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('serial', models.SlugField(unique=True, max_length=64, help_text='Unique identifier of the product', verbose_name='S/N')),
                ('photo', libs.stdimage.fields.StdImageField(variations={'admin': {'size': (200, 200), 'crop': False}, 'small': {'size': (160, 160), 'crop': False}, 'admin_micro': {'background': (255, 255, 255, 255), 'size': (60, 60), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}}, storage=libs.media_storage.MediaStorage('shop/product'), aspects=(), upload_to='', verbose_name='photo', min_dimensions=(180, 60))),
                ('photo_crop', models.CharField(editable=False, blank=True, max_length=32, verbose_name='stored_crop')),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='immediate_products')),
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
            field=models.ForeignKey(to='shop.ShopOrder', verbose_name='order', related_name='order_products'),
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
