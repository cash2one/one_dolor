# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0027_auto_20160417_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='mer_thume_img',
            field=models.ImageField(default='', upload_to=b'imgs/', verbose_name='\u5546\u54c1\u7f29\u7565\u56fe\u56fe\u7247(300*300)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='mer_img',
            field=models.ImageField(upload_to=b'imgs/', verbose_name='\u5546\u54c1\u56fe\u7247(330*330)'),
            preserve_default=True,
        ),
    ]
