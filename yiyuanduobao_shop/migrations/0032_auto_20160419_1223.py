# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0031_auto_20160419_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotteryresult',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
