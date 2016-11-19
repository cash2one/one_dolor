# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0068_shop_shop_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='cert_back_link',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u8054\u7cfb\u4eba\u8bc1\u4ef6\u53cd\u9762\u7167\u7247\u5b58\u50a8\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='cert_front_link',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u8054\u7cfb\u4eba\u8bc1\u4ef6\u6b63\u9762\u7167\u7247\u5b58\u50a8\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_img_oss_link',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u5e97\u94fa\u5c55\u793a\u56fe\u7247\u5b58\u50a8\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
