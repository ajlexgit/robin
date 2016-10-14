# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('code', models.CharField(verbose_name='code', unique=True, validators=[django.core.validators.MinLengthValidator(4)], max_length=24)),
                ('strategy_name', models.CharField(choices=[('fixed_amount', 'Fixed monetary amount'), ('percent', 'Percentage discount')], max_length=64, verbose_name='action')),
                ('parameter', models.CharField(blank=True, default='0', max_length=32, verbose_name='parameter')),
                ('redemption_limit', models.PositiveIntegerField(default=1, help_text='zero sets the limit to unlimited', verbose_name='redemption limit')),
                ('start_date', models.DateTimeField(blank=True, verbose_name='start time', null=True)),
                ('end_date', models.DateTimeField(blank=True, verbose_name='end time', null=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name_plural': 'promo codes',
                'verbose_name': 'promo code',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='PromoCodeReference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('applied', models.BooleanField(editable=False, default=False, verbose_name='applied')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
                ('promocode', models.ForeignKey(related_name='references', to='promocodes.PromoCode', verbose_name='promo code')),
            ],
            options={
                'verbose_name_plural': 'promo code references',
                'verbose_name': 'promo code reference',
                'ordering': ('-created',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='promocodereference',
            unique_together=set([('promocode', 'content_type', 'object_id')]),
        ),
    ]
