# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0039_auto_20160422_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='yiyuanduobao_shop.ItemType', null=True),
            preserve_default=True,
        ),
    ]
