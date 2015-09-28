# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import libs.media_storage
import ckeditor.fields
import django.utils.timezone
import libs.autoslug
import libs.stdimage.fields
import libs.valute_field.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('is_visible', models.BooleanField(default=False, db_index=True, verbose_name='visible')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='shop.ShopCategory', null=True, verbose_name='parent category', related_name='children')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
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
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(editable=False, verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)])),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
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
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('serial', models.SlugField(help_text='Unique identifier of the product', verbose_name='S/N', unique=True, max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(180, 60), storage=libs.media_storage.MediaStorage('shop/product'), upload_to='', verbose_name='photo', variations={'admin': {'size': (200, 200), 'crop': False}, 'small': {'size': (120, 120), 'crop': False}, 'admin_micro': {'size': (60, 60), 'background': (255, 255, 255, 255), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}}, aspects=())),
                ('photo_crop', models.CharField(blank=True, verbose_name='stored_crop', editable=False, max_length=32)),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='products')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='shopproduct',
            index_together=set([('category', 'is_visible')]),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(to='shop.ShopOrder', verbose_name='order', related_name='order_products'),
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
