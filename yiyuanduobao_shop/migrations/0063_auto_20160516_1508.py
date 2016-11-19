# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0062_auto_20160516_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopmanager',
            name='agent_name',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe4\xbb\xa3\xe7\x90\x86\xe5\x95\x86\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopmanager',
            name='shop',
            field=models.OneToOneField(related_name='shop_owner', null=True, blank=True, to='yiyuanduobao_shop.Shop', verbose_name=b'\xe7\xae\xa1\xe7\x90\x86\xe7\x9a\x84\xe5\xba\x97\xe9\x93\xba'),
            preserve_default=True,
        ),
    ]
