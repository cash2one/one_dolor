# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0041_merchant_commission_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='addr',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='take_part_num',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xb2\xe5\x8f\x82\xe4\xb8\x8e\xe7\x9a\x84\xe4\xbb\xb7\xe6\xa0\xbc'),
            preserve_default=True,
        ),
    ]
