# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0058_item_proxy_sale_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='mer_img_oss_link',
            field=models.CharField(max_length=500, null=True, verbose_name='\u5546\u54c1\u56fe\u7247\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='merchant',
            name='mer_thume_img_oss_link',
            field=models.CharField(max_length=500, null=True, verbose_name='\u5546\u54c1\u7f29\u7565\u56fe\u7247\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
