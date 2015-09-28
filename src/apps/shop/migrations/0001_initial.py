# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.valute_field.fields
import libs.media_storage
import libs.autoslug
import mptt.fields
import libs.stdimage.fields
import django.core.validators
import ckeditor.fields


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
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='parent category', null=True, to='shop.ShopCategory', blank=True, related_name='children')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Not paid'), (2, 'Paid')], default=1)),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', editable=False, validators=[django.core.validators.MinValueValidator(0)])),
                ('session', models.CharField(verbose_name='session', max_length=64, editable=False)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('-date',),
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('serial', models.SlugField(unique=True, verbose_name='S/N', max_length=64, help_text='Unique identifier of the product')),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), verbose_name='photo', variations={'admin': {'size': (200, 200), 'crop': False}, 'admin_micro': {'size': (60, 60), 'background': (255, 255, 255, 255), 'crop': False}, 'small': {'size': (120, 120), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}}, storage=libs.media_storage.MediaStorage('shop/product'), min_dimensions=(180, 60), upload_to='')),
                ('photo_crop', models.CharField(blank=True, verbose_name='stored_crop', max_length=32, editable=False)),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('category', models.ForeignKey(verbose_name='category', to='shop.ShopCategory', related_name='products')),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ('is_visible', 'sort_order'),
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(verbose_name='order', to='shop.ShopOrder', related_name='order_products'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.ShopProduct'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set([('order', 'product')]),
        ),
    ]
