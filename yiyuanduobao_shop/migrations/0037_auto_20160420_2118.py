# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0036_auto_20160420_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='banner_img',
        ),
        migrations.AddField(
            model_name='merchantbannerimg',
            name='merchant',
            field=models.ForeignKey(verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe5\x95\x86\xe5\x93\x81', blank=True, to='yiyuanduobao_shop.Merchant', null=True),
            preserve_default=True,
        ),
    ]
