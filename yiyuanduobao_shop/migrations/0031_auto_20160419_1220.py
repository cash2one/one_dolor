# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0030_lotteryresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotteryresult',
            name='create_time',
            field=models.DateTimeField(default='1987-01-13', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lotteryresult',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
