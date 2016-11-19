# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0046_auto_20160502_2235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticemsg',
            options={'verbose_name': '\u6d88\u606f', 'verbose_name_plural': '\u6d88\u606f'},
        ),
        migrations.AddField(
            model_name='noticemsg',
            name='create_time',
            field=models.DateTimeField(default='1987-01-01', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noticemsg',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
