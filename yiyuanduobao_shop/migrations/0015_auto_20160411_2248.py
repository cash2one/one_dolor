# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0014_customer_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-create_time'], 'verbose_name': '\u8d26\u6237', 'verbose_name_plural': '\u8d26\u6237'},
        ),
        migrations.AddField(
            model_name='account',
            name='create_time',
            field=models.DateTimeField(default='1990-11-11', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
