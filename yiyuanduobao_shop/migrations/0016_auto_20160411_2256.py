# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0015_auto_20160411_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='account',
            field=models.ForeignKey(verbose_name=b'\xe8\xb4\xa6\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Account', null=True),
            preserve_default=True,
        ),
    ]
