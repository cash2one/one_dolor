# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0037_auto_20160420_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_login_shop',
            field=models.ForeignKey(verbose_name=b'\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe7\x9a\x84\xe5\xba\x97', blank=True, to='yiyuanduobao_shop.Shop', null=True),
            preserve_default=True,
        ),
    ]
