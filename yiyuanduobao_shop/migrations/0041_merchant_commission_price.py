# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0040_item_item_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='commission_price',
            field=models.FloatField(default=0.0, verbose_name='\u4ee3\u5356\u4f63\u91d1'),
            preserve_default=True,
        ),
    ]
