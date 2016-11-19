# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0066_auto_20160524_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='cert_back',
            field=models.ImageField(upload_to=b'imgs/', null=True, verbose_name='\u8054\u7cfb\u4eba\u8bc1\u4ef6\u996d\u9762\u7167\u7247', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='cert_front',
            field=models.ImageField(upload_to=b'imgs/', null=True, verbose_name='\u8054\u7cfb\u4eba\u8bc1\u4ef6\u6b63\u9762\u7167\u7247', blank=True),
            preserve_default=True,
        ),
    ]
