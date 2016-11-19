# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0020_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['-create_time'], 'verbose_name': '\u6536\u8d27\u5730\u5740', 'verbose_name_plural': '\u6536\u8d27\u5730\u5740'},
        ),
        migrations.AddField(
            model_name='address',
            name='create_time',
            field=models.DateTimeField(default='1981-11-11', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
