# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0002_auto_20160409_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_code',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u671f\u53f7'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='winner_code',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u4e2d\u5956\u53f7\u7801'),
            preserve_default=True,
        ),
    ]
