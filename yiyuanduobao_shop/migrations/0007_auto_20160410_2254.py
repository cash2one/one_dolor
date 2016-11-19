# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0006_auto_20160410_2238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchant',
            options={'ordering': ['create_time'], 'verbose_name': '\u5546\u54c1', 'verbose_name_plural': '\u5546\u54c1'},
        ),
        migrations.AddField(
            model_name='merchantbannerimg',
            name='create_time',
            field=models.DateTimeField(default='1990-11-11', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='merchantbannerimg',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='banner_img',
            field=models.ManyToManyField(to='yiyuanduobao_shop.MerchantBannerImg', null=True, verbose_name=b'\xe8\xbd\xae\xe6\x92\xad\xe5\x9b\xbe\xe7\x89\x87', blank=True),
            preserve_default=True,
        ),
    ]
