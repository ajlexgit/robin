# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import mptt.fields
import django.core.validators
import libs.media_storage
import libs.valute_field.fields
import libs.stdimage.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per item')),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, null=True, verbose_name='parent category', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], default=1, verbose_name='status')),
                ('pay_date', models.DateTimeField(null=True, editable=False, verbose_name='pay date')),
                ('products_cost', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], editable=False, verbose_name='products cost')),
                ('session', models.CharField(max_length=64, editable=False, verbose_name='session')),
                ('date', models.DateTimeField(editable=False, verbose_name='create date')),
            ],
            options={
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('serial', models.SlugField(max_length=64, verbose_name='S/N', unique=True, help_text='Unique identifier of the product')),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), min_dimensions=(180, 60), aspects=(), variations={'small': {'crop': False, 'size': (120, 120)}, 'admin_micro': {'background': (255, 255, 255, 255), 'crop': False, 'size': (60, 60)}, 'admin': {'crop': False, 'size': (200, 200)}, 'normal': {'crop': False, 'size': (300, 300)}}, upload_to='', verbose_name='photo')),
                ('photo_crop', models.CharField(max_length=32, editable=False, verbose_name='stored_crop', blank=True)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('category', models.ForeignKey(related_name='products', to='shop.ShopCategory', verbose_name='category')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
                'ordering': ('is_visible', 'sort_order'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(related_name='order_products', to='shop.ShopOrder', verbose_name='order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(to='shop.ShopProduct', verbose_name='product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set([('order', 'product')]),
        ),
    ]
