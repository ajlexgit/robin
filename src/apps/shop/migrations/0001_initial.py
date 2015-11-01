# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.valute_field.fields
import django.core.validators
import libs.autoslug
import mptt.fields
import django.utils.timezone
import libs.media_storage
import ckeditor.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', db_index=True, default=False)),
                ('product_count', models.PositiveIntegerField(help_text='count of immediate visible products', editable=False, default=0)),
                ('total_product_count', models.PositiveIntegerField(help_text='count of visible products', editable=False, default=0)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='parent category', related_name='children', null=True, blank=True, to='shop.ShopCategory')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(1, 'Not paid'), (2, 'Paid')])),
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
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('serial', models.SlugField(verbose_name='serial number', help_text='Unique identifier of the product', max_length=64, unique=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='photo', upload_to='', min_dimensions=(180, 60), storage=libs.media_storage.MediaStorage('shop/product'), aspects=(), variations={'admin': {'crop': False, 'size': (200, 200)}, 'small': {'crop': False, 'size': (160, 160)}, 'admin_micro': {'crop': False, 'size': (60, 60), 'background': (255, 255, 255, 255)}, 'normal': {'crop': False, 'size': (300, 300)}})),
                ('photo_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', editable=False, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(verbose_name='category', related_name='immediate_products', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ('-created',),
                'verbose_name_plural': 'products',
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
