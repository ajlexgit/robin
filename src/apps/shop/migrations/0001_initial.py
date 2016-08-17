# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.valute_field.fields
import mptt.fields
import libs.storages.media_storage
import django.core.validators
import django.utils.timezone
import uuid
import libs.autoslug
import ckeditor.fields
import gallery.models
import django.db.models.deletion
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyReceiver',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
            ],
            options={
                'verbose_name_plural': 'notify receivers',
                'verbose_name': 'notify receiver',
            },
        ),
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order_price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per unit')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from='title')),
                ('is_visible', models.BooleanField(default=True, verbose_name='visible', db_index=True)),
                ('product_count', models.PositiveIntegerField(default=0, help_text='count of immediate visible products', editable=False)),
                ('total_product_count', models.PositiveIntegerField(default=0, help_text='count of visible products', editable=False)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(null=True, related_name='children', blank=True, verbose_name='parent category', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='UUID')),
                ('session', models.CharField(max_length=64, editable=False, verbose_name='session')),
                ('is_confirmed', models.BooleanField(default=False, help_text='Confirmed by the user', editable=False, verbose_name='confirmed')),
                ('confirm_date', models.DateTimeField(null=True, editable=False, verbose_name='confirm date')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='cancelled')),
                ('cancel_date', models.DateTimeField(null=True, editable=False, verbose_name='cancel date')),
                ('is_checked', models.BooleanField(default=False, verbose_name='checked')),
                ('check_date', models.DateTimeField(null=True, editable=False, verbose_name='check date')),
                ('is_paid', models.BooleanField(default=False, verbose_name='paid')),
                ('pay_date', models.DateTimeField(null=True, editable=False, verbose_name='pay date')),
                ('is_archived', models.BooleanField(default=False, verbose_name='archived')),
                ('archivation_date', models.DateTimeField(null=True, editable=False, verbose_name='archivation date')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='create date')),
            ],
            options={
                'verbose_name_plural': 'orders',
                'ordering': ('-created',),
                'verbose_name': 'order',
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from='title')),
                ('serial', models.SlugField(max_length=64, verbose_name='serial number', unique=True, help_text='Unique identifier of the product')),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(default=True, verbose_name='visible')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(related_name='immediate_products', verbose_name='category', to='shop.ShopCategory')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, blank=True, editable=False, verbose_name='stored_crop')),
            ],
            options={
                'verbose_name_plural': 'image items',
                'ordering': ('object_id', 'sort_order', 'created'),
                'default_permissions': (),
                'abstract': False,
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, verbose_name='gallery', to='shop.ShopProductGallery'),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='order',
            field=models.ForeignKey(related_name='records', verbose_name='order', to='shop.ShopOrder'),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='product',
            field=models.ForeignKey(to='shop.ShopProduct', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='notifyreceiver',
            name='config',
            field=models.ForeignKey(related_name='receivers', to='shop.ShopConfig'),
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
