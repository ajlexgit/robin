# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import ckeditor.fields
import libs.media_storage
import libs.stdimage.fields
import libs.valute_field.fields
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', unique=True, populate_from=('title',))),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('sort_order', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'category',
                'ordering': ('is_visible', 'sort_order'),
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not paid'), (2, 'Paid')], default=1, verbose_name='status')),
                ('pay_date', models.DateTimeField(editable=False, verbose_name='pay date', null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', editable=False, validators=[django.core.validators.MinValueValidator(0)])),
                ('hash', models.CharField(unique=True, editable=False, validators=[django.core.validators.RegexValidator('^[0-9a-f]{32}$')], verbose_name='hash', max_length=32)),
                ('session', models.CharField(editable=False, verbose_name='session', max_length=64)),
                ('date', models.DateTimeField(editable=False, verbose_name='create date')),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('-date',),
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per item')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', unique=True, populate_from=('title',))),
                ('serial', models.SlugField(help_text='Unique identifier of the product', unique=True, verbose_name='S/N', max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to='', verbose_name='photo', min_dimensions=(200, 0), variations={'small': {'crop': False, 'stretch': False, 'size': (100, 100)}, 'normal': {'crop': False, 'stretch': False, 'size': (450, 450)}}, aspects=(), storage=libs.media_storage.MediaStorage('shop'))),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('sort_order', models.PositiveIntegerField()),
                ('categories', models.ManyToManyField(related_name='products', verbose_name='categories', to='shop.Category')),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ('is_visible', 'sort_order'),
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
