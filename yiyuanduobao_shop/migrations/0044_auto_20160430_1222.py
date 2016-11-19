# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0043_auto_20160428_0229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='last_login_shop',
        ),
        migrations.AddField(
            model_name='customer',
            name='shops',
            field=models.ManyToManyField(to='yiyuanduobao_shop.Shop', null=True, verbose_name=b'\xe6\x98\xaf\xe5\x93\xaa\xe4\xba\x9b\xe5\xba\x97\xe7\x9a\x84\xe4\xbc\x9a\xe5\x91\x98', blank=True),
            preserve_default=True,
        ),
    ]
