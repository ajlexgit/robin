# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import ckeditor.fields
import libs.valute_field.fields
import django.core.validators
import libs.media_storage
import mptt.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', verbose_name='parent category', null=True, to='shop.Category')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], default=1, verbose_name='status')),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], editable=False, verbose_name='products cost')),
                ('hash', models.CharField(verbose_name='hash', max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-f]{32}$')], editable=False)),
                ('session', models.CharField(verbose_name='session', max_length=64, editable=False)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('serial', models.SlugField(max_length=64, unique=True, help_text='Unique identifier of the product', verbose_name='S/N')),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), verbose_name='photo', variations={'admin': {'crop': False, 'size': (200, 200)}, 'small': {'size': (120, 120)}, 'normal': {'crop': False, 'size': (300, 300)}}, aspects=(), min_dimensions=(180, 180), upload_to='')),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('categories', models.ManyToManyField(verbose_name='categories', related_name='products', to='shop.Category')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(to='shop.Product', verbose_name='product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set([('order', 'product')]),
        ),
    ]
