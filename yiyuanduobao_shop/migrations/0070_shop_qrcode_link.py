# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0069_auto_20160524_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='qrcode_link',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u5e97\u94fa\u4e8c\u7ef4\u7801', blank=True),
            preserve_default=True,
        ),
    ]
