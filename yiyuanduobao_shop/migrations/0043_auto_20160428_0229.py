# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0042_auto_20160424_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='winner_lottery_result',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u4e2d\u5956\u5bf9\u5e94\u65f6\u65f6\u5f69\u53f7\u7801'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lotteryticket',
            name='item',
            field=models.ForeignKey(related_name='LotteryItem', verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe9\xa1\xb9\xe7\x9b\xae', to='yiyuanduobao_shop.Item'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lotteryticket',
            name='order',
            field=models.ForeignKey(related_name='LotteryOrder', verbose_name='\u5bf9\u5e94\u8ba2\u5355', to='yiyuanduobao_shop.Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='addr',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe5\x9c\xb0\xe5\x9d\x80'),
            preserve_default=True,
        ),
    ]
