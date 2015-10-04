# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import django.utils.timezone
import libs.stdimage.fields
import ckeditor.fields
import libs.media_storage
import libs.valute_field.fields
import mptt.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('is_visible', models.BooleanField(verbose_name='visible', db_index=True, default=False)),
                ('product_count', models.PositiveIntegerField(default=0, editable=False, help_text='count of immediate visible products')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='shop.ShopCategory', null=True, blank=True, verbose_name='parent category', related_name='children')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
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
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(1, 'Not paid'), (2, 'Paid')])),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='products cost', editable=False)),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('serial', models.SlugField(verbose_name='S/N', help_text='Unique identifier of the product', max_length=64, unique=True)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(180, 60), aspects=(), storage=libs.media_storage.MediaStorage('shop/product'), verbose_name='photo', variations={'normal': {'size': (300, 300), 'crop': False}, 'admin_micro': {'background': (255, 255, 255, 255), 'size': (60, 60), 'crop': False}, 'admin': {'size': (200, 200), 'crop': False}, 'small': {'size': (160, 160), 'crop': False}})),
                ('photo_crop', models.CharField(blank=True, verbose_name='stored_crop', editable=False, max_length=32)),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='immediate_products')),
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
