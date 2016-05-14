# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.autoslug
import django.utils.timezone
import libs.valute_field.fields
import gallery.models
import libs.storages
import django.core.validators
import ckeditor.fields
import mptt.fields
import django.db.models.deletion
import uuid
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyReciever',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail')),
            ],
            options={
                'verbose_name': 'notify reciever',
                'verbose_name_plural': 'notify recievers',
            },
        ),
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('order_price', libs.valute_field.fields.ValuteField(verbose_name='price per unit', validators=[django.core.validators.MinValueValidator(0)])),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False, db_index=True)),
                ('product_count', models.PositiveIntegerField(default=0, help_text='count of immediate visible products', editable=False)),
                ('total_product_count', models.PositiveIntegerField(default=0, help_text='count of visible products', editable=False)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='shop.ShopCategory', null=True, verbose_name='parent category', related_name='children', blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=128, verbose_name='header')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('uuid', models.UUIDField(verbose_name='UUID', default=uuid.uuid4, editable=False, unique=True)),
                ('session', models.CharField(max_length=64, verbose_name='session', editable=False)),
                ('is_confirmed', models.BooleanField(verbose_name='confirmed', default=False, help_text='Confirmed by the user', editable=False)),
                ('confirm_date', models.DateTimeField(verbose_name='confirm date', editable=False, null=True)),
                ('is_cancelled', models.BooleanField(verbose_name='cancelled', default=False)),
                ('cancel_date', models.DateTimeField(verbose_name='cancel date', editable=False, null=True)),
                ('is_checked', models.BooleanField(verbose_name='checked', default=False)),
                ('check_date', models.DateTimeField(verbose_name='check date', editable=False, null=True)),
                ('is_paid', models.BooleanField(verbose_name='paid', default=False)),
                ('pay_date', models.DateTimeField(verbose_name='pay date', editable=False, null=True)),
                ('is_archived', models.BooleanField(verbose_name='archived', default=False)),
                ('archivation_date', models.DateTimeField(verbose_name='archivation date', editable=False, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, verbose_name='alias', populate_from=('title',))),
                ('serial', models.SlugField(max_length=64, verbose_name='serial number', help_text='Unique identifier of the product', unique=True)),
                ('description', ckeditor.fields.CKEditorField(verbose_name='description', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('is_visible', models.BooleanField(verbose_name='visible', default=False)),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(verbose_name='category', related_name='immediate_products', to='shop.ShopCategory')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ShopProductGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', storage=libs.storages.MediaStorage())),
                ('image_crop', models.CharField(max_length=32, verbose_name='stored_crop', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, to='shop.ShopProductGallery', null=True, verbose_name='gallery', blank=True),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='order',
            field=models.ForeignKey(verbose_name='order', related_name='records', to='shop.ShopOrder'),
        ),
        migrations.AddField(
            model_name='orderrecord',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.ShopProduct'),
        ),
        migrations.AddField(
            model_name='notifyreciever',
            name='config',
            field=models.ForeignKey(related_name='recievers', to='shop.ShopConfig'),
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
