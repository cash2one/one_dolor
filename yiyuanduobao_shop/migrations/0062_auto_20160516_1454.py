# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0061_shopbanner_banner_oss_img_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopmanager',
            name='agent_shops',
            field=models.ManyToManyField(related_name='agent_shops', null=True, verbose_name=b'\xe4\xbb\xa3\xe7\x90\x86\xe7\x9a\x84\xe5\xba\x97\xe9\x93\xba', to='yiyuanduobao_shop.Shop', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopmanager',
            name='shop',
            field=models.OneToOneField(related_name='shop_owner', verbose_name=b'\xe7\xae\xa1\xe7\x90\x86\xe7\x9a\x84\xe5\xba\x97\xe9\x93\xba', to='yiyuanduobao_shop.Shop'),
            preserve_default=True,
        ),
    ]
