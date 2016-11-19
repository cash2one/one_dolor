# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0060_merchantbannerimg_img_oss_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopbanner',
            name='banner_oss_img_link',
            field=models.CharField(max_length=1000, null=True, verbose_name='banner\u56fe\u5b58\u50a8\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
