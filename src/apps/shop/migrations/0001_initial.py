# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import ckeditor.fields
import libs.valute_field.fields
import gallery.models
import django.db.models.deletion
import gallery.fields
import mptt.fields
import django.utils.timezone
import django.core.validators
import libs.media_storage
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReciever',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
            ],
            options={
                'verbose_name_plural': 'e-mail recievers',
                'verbose_name': 'e-mail reciever',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item', validators=[django.core.validators.MinValueValidator(0)])),
                ('count', models.PositiveSmallIntegerField(verbose_name='count')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('is_visible', models.BooleanField(db_index=True, verbose_name='visible', default=False)),
                ('product_count', models.PositiveIntegerField(editable=False, help_text='count of immediate visible products', default=0)),
                ('total_product_count', models.PositiveIntegerField(editable=False, help_text='count of visible products', default=0)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='shop.ShopCategory', verbose_name='parent category', null=True, blank=True, related_name='children')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('uuid', models.UUIDField(editable=False, verbose_name='UUID', unique=True, default=uuid.uuid4)),
                ('session', models.CharField(max_length=64, editable=False, verbose_name='session')),
                ('products_cost', libs.valute_field.fields.ValuteField(editable=False, verbose_name='products cost', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_confirmed', models.BooleanField(editable=False, verbose_name='confirmed', help_text='Confirmed by the user', default=False)),
                ('confirm_date', models.DateTimeField(editable=False, verbose_name='confirm date', null=True)),
                ('is_cancelled', models.BooleanField(verbose_name='cancelled', default=False)),
                ('cancel_date', models.DateTimeField(editable=False, verbose_name='cancel date', null=True)),
                ('is_checked', models.BooleanField(verbose_name='checked', default=False)),
                ('check_date', models.DateTimeField(editable=False, verbose_name='check date', null=True)),
                ('is_paid', models.BooleanField(verbose_name='paid', default=False)),
                ('pay_date', models.DateTimeField(editable=False, verbose_name='pay date', null=True)),
                ('is_archived', models.BooleanField(verbose_name='archived', default=False)),
                ('archivation_date', models.DateTimeField(editable=False, verbose_name='archivation date', null=True)),
                ('date', models.DateTimeField(editable=False, verbose_name='create date')),
            ],
            options={
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), verbose_name='alias', unique=True)),
                ('serial', models.SlugField(max_length=64, verbose_name='serial number', unique=True, help_text='Unique identifier of the product')),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(to='shop.ShopCategory', verbose_name='category', related_name='immediate_products')),
            ],
            options={
                'verbose_name_plural': 'products',
                'ordering': ('-created',),
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGallery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(max_length=32, blank=True, editable=False, verbose_name='stored_crop')),
            ],
            options={
                'verbose_name_plural': 'image items',
                'abstract': False,
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(verbose_name='gallery', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shop.ShopProductGallery'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(to='shop.ShopOrder', verbose_name='order', related_name='order_products'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.ShopProduct'),
        ),
        migrations.AddField(
            model_name='emailreciever',
            name='config',
            field=models.ForeignKey(to='shop.ShopConfig', related_name='recievers'),
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
