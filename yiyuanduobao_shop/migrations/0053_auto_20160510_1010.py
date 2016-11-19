# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0052_shopbanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopbanner',
            name='banner_link',
            field=models.CharField(default=b'#', max_length=1000, null=True, verbose_name='banner\u94fe\u63a5\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
