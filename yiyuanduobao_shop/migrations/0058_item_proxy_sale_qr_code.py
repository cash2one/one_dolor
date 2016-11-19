# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0057_item_winner_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='proxy_sale_qr_code',
            field=models.CharField(default=b'', max_length=500, verbose_name='\u672c\u671f\u4ee3\u5356\u4e8c\u7ef4\u7801'),
            preserve_default=True,
        ),
    ]
