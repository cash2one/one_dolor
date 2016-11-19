# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0054_shopbanner_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='lottery_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe4\xb8\xad\xe5\xa5\x96\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
    ]
