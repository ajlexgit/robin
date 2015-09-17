# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import libs.stdimage.fields
import libs.media_storage
import libs.valute_field.fields
import django.core.validators
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not payed'), (2, 'Payed')], verbose_name='status', default=1)),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', editable=False, validators=[django.core.validators.MinValueValidator(0)])),
                ('hash', models.CharField(validators=[django.core.validators.RegexValidator('^[0-9a-f]{32}$')], verbose_name='hash', unique=True, max_length=32, editable=False)),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
                ('order', models.ForeignKey(verbose_name='order', related_name='order_products', to='shop.Order')),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from=('title',), unique=True)),
                ('serial', models.SlugField(max_length=64, verbose_name='S/N', unique=True, help_text='Unique identifier of the product')),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(200, 0), verbose_name='photo', aspects=(), upload_to='', variations={'normal': {'crop': False, 'size': (450, 450), 'stretch': False}, 'small': {'crop': False, 'size': (100, 100), 'stretch': False}}, storage=libs.media_storage.MediaStorage('shop'))),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('order', models.PositiveIntegerField()),
                ('categories', models.ManyToManyField(verbose_name='categories', related_name='products', to='shop.Category')),
            ],
            options={
                'ordering': ('is_visible', 'order'),
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
