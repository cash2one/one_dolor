# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0024_customer_investor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_no',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u8ba2\u5355\u53f7'),
            preserve_default=True,
        ),
    ]
