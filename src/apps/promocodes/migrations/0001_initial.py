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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('code', models.CharField(validators=[django.core.validators.MinLengthValidator(4)], verbose_name='code', max_length=24, unique=True)),
                ('strategy_name', models.CharField(verbose_name='action', choices=[('fixed_amount', 'Fixed monetary amount'), ('percent', 'Percentage discount')], max_length=64)),
                ('parameter', models.CharField(verbose_name='parameter', default='0', blank=True, max_length=32)),
                ('redemption_limit', models.PositiveIntegerField(verbose_name='redemption limit', default=1, help_text='zero sets the limit to unlimited')),
                ('start_date', models.DateTimeField(null=True, verbose_name='start time', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='end time', blank=True)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'promo codes',
                'verbose_name': 'promo code',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='PromoCodeUsage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(verbose_name='created on', editable=False, default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
                ('promocode', models.ForeignKey(verbose_name='promo code', related_name='usages', to='promocodes.PromoCode')),
            ],
            options={
                'verbose_name_plural': 'promo code usages',
                'verbose_name': 'promo code usage',
                'ordering': ('-created',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='promocodeusage',
            unique_together=set([('promocode', 'content_type', 'object_id')]),
        ),
    ]
