# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0067_auto_20160524_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_img',
            field=models.ImageField(upload_to=b'imgs/', null=True, verbose_name='\u5e97\u94fa\u5c55\u793a\u56fe\u7247', blank=True),
            preserve_default=True,
        ),
    ]
