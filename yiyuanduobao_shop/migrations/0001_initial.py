# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('mobile', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('openid', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_status', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe7\x8a\xb6\xe6\x80\x81')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('mer_type', models.IntegerField(default=0, verbose_name='\u5546\u54c1\u7c7b\u578b')),
                ('mer_img', models.ImageField(upload_to=b'imgs/', verbose_name='\u5546\u54c1\u56fe\u7247')),
                ('price_unit', models.IntegerField(default=1, verbose_name='\u5355\u4f4d\u4ef7\u683c')),
                ('share', models.IntegerField(default=1, verbose_name='\u5546\u54c1\u4efd\u6570')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_status', models.IntegerField(default=0, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(related_name='customer_order', to='yiyuanduobao_shop.Customer')),
                ('item', models.ForeignKey(related_name='item_order', to='yiyuanduobao_shop.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopManager',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('shop', models.OneToOneField(to='yiyuanduobao_shop.Shop')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='merchant',
            name='shop',
            field=models.ForeignKey(related_name='shop_merchant', to='yiyuanduobao_shop.Shop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='merchant',
            field=models.ForeignKey(related_name='merchant_item', to='yiyuanduobao_shop.Merchant'),
            preserve_default=True,
        ),
    ]
