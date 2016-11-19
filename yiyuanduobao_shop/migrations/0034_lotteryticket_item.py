# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0033_auto_20160419_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotteryticket',
            name='item',
            field=models.ForeignKey(default='', verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe9\xa1\xb9\xe7\x9b\xae', to='yiyuanduobao_shop.Item'),
            preserve_default=False,
        ),
    ]
