# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.fields
import django.core.validators
import gallery.models
import libs.media_storage
import mptt.fields
import libs.valute_field.fields
import uuid
import django.utils.timezone
import libs.autoslug
import django.db.models.deletion
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReciever',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
            ],
            options={
                'verbose_name': 'e-mail reciever',
                'verbose_name_plural': 'e-mail recievers',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order_price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price per item')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), unique=True, verbose_name='alias')),
                ('is_visible', models.BooleanField(db_index=True, default=False, verbose_name='visible')),
                ('product_count', models.PositiveIntegerField(default=0, editable=False, help_text='count of immediate visible products')),
                ('total_product_count', models.PositiveIntegerField(default=0, editable=False, help_text='count of visible products')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='shop.ShopCategory', null=True, verbose_name='parent category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('uuid', models.UUIDField(unique=True, verbose_name='UUID', default=uuid.uuid4, editable=False)),
                ('session', models.CharField(verbose_name='session', editable=False, max_length=64)),
                ('products_cost', libs.valute_field.fields.ValuteField(editable=False, validators=[django.core.validators.MinValueValidator(0)], verbose_name='products cost')),
                ('is_confirmed', models.BooleanField(verbose_name='confirmed', default=False, editable=False, help_text='Confirmed by the user')),
                ('confirm_date', models.DateTimeField(verbose_name='confirm date', null=True, editable=False)),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='cancelled')),
                ('cancel_date', models.DateTimeField(verbose_name='cancel date', null=True, editable=False)),
                ('is_checked', models.BooleanField(default=False, verbose_name='checked')),
                ('check_date', models.DateTimeField(verbose_name='check date', null=True, editable=False)),
                ('is_paid', models.BooleanField(default=False, verbose_name='paid')),
                ('pay_date', models.DateTimeField(verbose_name='pay date', null=True, editable=False)),
                ('is_archived', models.BooleanField(default=False, verbose_name='archived')),
                ('archivation_date', models.DateTimeField(verbose_name='archivation date', null=True, editable=False)),
                ('date', models.DateTimeField(verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('-date',),
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('alias', libs.autoslug.AutoSlugField(populate_from=('title',), unique=True, verbose_name='alias')),
                ('serial', models.SlugField(unique=True, verbose_name='serial number', max_length=64, help_text='Unique identifier of the product')),
                ('description', ckeditor.fields.CKEditorField(blank=True, verbose_name='description')),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('is_visible', models.BooleanField(default=False, verbose_name='visible')),
                ('created', models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('category', models.ForeignKey(related_name='immediate_products', to='shop.ShopCategory', verbose_name='category')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
            },
        ),
        migrations.CreateModel(
            name='ShopProductGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='gallery.GalleryItemBase', serialize=False, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', editable=False, max_length=32, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='gallery',
            field=gallery.fields.GalleryField(to='shop.ShopProductGallery', on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, verbose_name='gallery'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(related_name='order_products', to='shop.ShopOrder', verbose_name='order'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='product', to='shop.ShopProduct'),
        ),
        migrations.AddField(
            model_name='emailreciever',
            name='config',
            field=models.ForeignKey(related_name='recievers', to='shop.ShopConfig'),
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
