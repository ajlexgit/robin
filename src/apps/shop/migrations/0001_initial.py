# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.autoslug
import ckeditor.fields
import libs.media_storage
import django.core.validators
import libs.valute_field.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('sort_order', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('is_visible', 'sort_order'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Not paid'), (2, 'Paid')], default=1)),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(editable=False, validators=[django.core.validators.MinValueValidator(0)], verbose_name='products cost')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
                ('order', models.ForeignKey(related_name='order_products', to='shop.Order', verbose_name='order')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from=('title',), verbose_name='alias')),
                ('serial', models.SlugField(help_text='Unique identifier of the product', verbose_name='S/N', unique=True, max_length=64)),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(200, 0), aspects=(), variations={'normal': {'size': (450, 450), 'crop': False, 'stretch': False}, 'small': {'size': (100, 100), 'crop': False, 'stretch': False}}, storage=libs.media_storage.MediaStorage('shop'), verbose_name='photo', upload_to='')),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('sort_order', models.PositiveIntegerField()),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
