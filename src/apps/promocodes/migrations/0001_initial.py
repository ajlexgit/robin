# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(unique=True, verbose_name='code', validators=[django.core.validators.MinLengthValidator(4)], max_length=32)),
                ('strategy_name', models.CharField(verbose_name='strategy', choices=[('fixed_amount', 'Fixed amount'), ('percent', 'By a percent')], max_length=64)),
                ('parameter', models.CharField(verbose_name='parameter', blank=True, default='0', max_length=32)),
                ('redemption_limit', models.PositiveIntegerField(help_text='zero sets the limit to unlimited', default=1, verbose_name='redemption limit')),
                ('start_date', models.DateTimeField(verbose_name='start time', blank=True, null=True)),
                ('end_date', models.DateTimeField(verbose_name='end time', blank=True, null=True)),
                ('created', models.DateTimeField(verbose_name='created on', default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'promo code',
                'verbose_name_plural': 'promo codes',
            },
        ),
        migrations.CreateModel(
            name='PromoCodeUsage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(verbose_name='created on', default=django.utils.timezone.now, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
                ('promocode', models.ForeignKey(related_name='usages', to='promocodes.PromoCode', verbose_name='promo code')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'promo code usage',
                'verbose_name_plural': 'promo code usages',
            },
        ),
        migrations.AlterUniqueTogether(
            name='promocodeusage',
            unique_together=set([('promocode', 'content_type', 'object_id')]),
        ),
    ]
