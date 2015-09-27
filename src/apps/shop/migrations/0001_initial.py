# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.valute_field.fields
import libs.stdimage.fields
import mptt.fields
import libs.autoslug
import ckeditor.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', verbose_name='parent category', to='shop.Category', null=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(1, 'Not paid'), (2, 'Paid')])),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(editable=False, verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)])),
                ('hash', models.CharField(verbose_name='hash', validators=[django.core.validators.RegexValidator('^[0-9a-f]{32}$')], unique=True, editable=False, max_length=32)),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
                ('order', models.ForeignKey(related_name='order_products', verbose_name='order', to='shop.Order')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('serial', models.SlugField(verbose_name='S/N', help_text='Unique identifier of the product', unique=True, max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(variations={'small': {'crop': False, 'size': (120, 120)}, 'admin_micro': {'crop': False, 'background': (255, 255, 255, 255), 'size': (60, 60)}, 'normal': {'crop': False, 'size': (300, 300)}, 'admin': {'crop': False, 'size': (200, 200)}}, storage=libs.media_storage.MediaStorage('shop/product'), verbose_name='photo', aspects=(), upload_to='', min_dimensions=(180, 60))),
                ('photo_crop', models.CharField(verbose_name='stored_crop', editable=False, blank=True, max_length=32)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('categories', models.ManyToManyField(verbose_name='categories', to='shop.Category', related_name='products')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('is_visible', 'sort_order'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set([('order', 'product')]),
        ),
    ]
