# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import gallery.models
import django.db.models.deletion
import libs.storages.media_storage
import uuid
import gallery.fields
import django.utils.timezone
import ckeditor.fields
import libs.autoslug
import libs.valute_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
            ],
            options={
                'verbose_name': 'notification receiver',
                'verbose_name_plural': 'notification receivers',
            },
        ),
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per item')),
                ('count', models.PositiveIntegerField(verbose_name='quantity')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', unique=True, verbose_name='slug')),
                ('product_count', models.PositiveIntegerField(default=0, help_text='count of immediate visible products', editable=False)),
                ('total_product_count', models.PositiveIntegerField(default=0, help_text='count of visible products', editable=False)),
                ('is_visible', models.BooleanField(verbose_name='visible', default=True, db_index=True)),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('sort_order', models.IntegerField(verbose_name='order', default=0)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', verbose_name='parent category', to='shop.ShopCategory', null=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(verbose_name='UUID', default=uuid.uuid4, editable=False, unique=True)),
                ('session', models.CharField(verbose_name='session', max_length=64, editable=False)),
                ('is_confirmed', models.BooleanField(verbose_name='confirmed', default=False, editable=False)),
                ('confirm_date', models.DateTimeField(verbose_name='confirm date', null=True, editable=False)),
                ('is_cancelled', models.BooleanField(verbose_name='cancelled', default=False)),
                ('cancel_date', models.DateTimeField(verbose_name='cancel date', null=True, editable=False)),
                ('is_checked', models.BooleanField(verbose_name='checked', default=False)),
                ('check_date', models.DateTimeField(verbose_name='check date', null=True, editable=False)),
                ('is_paid', models.BooleanField(verbose_name='paid', default=False)),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('is_archived', models.BooleanField(verbose_name='archived', default=False)),
                ('archivation_date', models.DateTimeField(verbose_name='archivation date', null=True, editable=False)),
                ('products_cost', libs.valute_field.fields.ValuteField(verbose_name='products cost', editable=False)),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', unique=True, verbose_name='slug')),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price')),
                ('is_visible', models.BooleanField(verbose_name='visible', default=True)),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(related_name='immediate_products', verbose_name='category', to='shop.ShopCategory')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'gallery',
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, to='gallery.GalleryItemBase', primary_key=True, parent_link=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage())),
                ('image_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
            ],
            options={
                'verbose_name': 'image item',
                'abstract': False,
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'image items',
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(blank=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', to='shop.ShopProductGallery', null=True),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='order',
            field=models.ForeignKey(related_name='records', verbose_name='order', to='shop.ShopOrder'),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='product', to='shop.ShopProduct', null=True),
        ),
        migrations.AddField(
            model_name='notifyreceiver',
            name='config',
            field=models.ForeignKey(to='shop.ShopConfig', related_name='receivers'),
        ),
        migrations.AlterIndexTogether(
            name='shopproduct',
            index_together=set([('category', 'is_visible')]),
        ),
        migrations.AlterUniqueTogether(
            name='orderrecord',
            unique_together=set([('order', 'product')]),
        ),
    ]
