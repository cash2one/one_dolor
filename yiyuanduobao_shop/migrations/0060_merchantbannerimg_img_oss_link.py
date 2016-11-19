# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0059_auto_20160515_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantbannerimg',
            name='img_oss_link',
            field=models.CharField(max_length=500, null=True, verbose_name='\u5546\u54c1\u8f6e\u64ad\u56fe\u94fe\u63a5', blank=True),
            preserve_default=True,
        ),
    ]
