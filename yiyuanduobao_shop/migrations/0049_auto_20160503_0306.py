# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0048_noticemsg_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticemsg',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='noticemsg',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
    ]
