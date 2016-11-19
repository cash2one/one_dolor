# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0065_merchantbannerimg_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantbannerimg',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchantbannerimg',
            name='shop',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x95\x86\xe5\xba\x97', blank=True, to='yiyuanduobao_shop.Shop', null=True),
            preserve_default=True,
        ),
    ]
