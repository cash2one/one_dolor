# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0064_auto_20160523_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantbannerimg',
            name='shop',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x95\x86\xe5\x93\x81', blank=True, to='yiyuanduobao_shop.Shop', null=True),
            preserve_default=True,
        ),
    ]
