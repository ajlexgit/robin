# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gallery.fields
import libs.storages.media_storage
import gallery.models
import libs.autoslug
import django.utils.timezone
import mptt.fields
import uuid
import ckeditor.fields
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
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per unit')),
                ('count', models.PositiveIntegerField(verbose_name='count')),
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
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug', unique=True)),
                ('product_count', models.PositiveIntegerField(help_text='count of immediate visible products', default=0, editable=False)),
                ('total_product_count', models.PositiveIntegerField(help_text='count of visible products', default=0, editable=False)),
                ('is_visible', models.BooleanField(db_index=True, default=True, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('sort_order', models.IntegerField(default=0, verbose_name='order')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(verbose_name='parent category', null=True, related_name='children', blank=True, to='shop.ShopCategory')),
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
                ('uuid', models.UUIDField(editable=False, unique=True, default=uuid.uuid4, verbose_name='UUID')),
                ('session', models.CharField(max_length=64, editable=False, verbose_name='session')),
                ('is_confirmed', models.BooleanField(help_text='Confirmed by the user', editable=False, default=False, verbose_name='confirmed')),
                ('confirm_date', models.DateTimeField(null=True, editable=False, verbose_name='confirm date')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='cancelled')),
                ('cancel_date', models.DateTimeField(null=True, editable=False, verbose_name='cancel date')),
                ('is_checked', models.BooleanField(default=False, verbose_name='checked')),
                ('check_date', models.DateTimeField(null=True, editable=False, verbose_name='check date')),
                ('is_paid', models.BooleanField(default=False, verbose_name='paid')),
                ('pay_date', models.DateTimeField(null=True, editable=False, verbose_name='pay date')),
                ('is_archived', models.BooleanField(default=False, verbose_name='archived')),
                ('archivation_date', models.DateTimeField(null=True, editable=False, verbose_name='archivation date')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='create date')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug', unique=True)),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price')),
                ('is_visible', models.BooleanField(default=True, verbose_name='visible')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='create date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('category', models.ForeignKey(verbose_name='category', related_name='immediate_products', to='shop.ShopCategory')),
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
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, editable=False, blank=True, verbose_name='stored_crop')),
            ],
            options={
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'image items',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', null=True, to='shop.ShopProductGallery', blank=True),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='order',
            field=models.ForeignKey(verbose_name='order', related_name='records', to='shop.ShopOrder'),
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
