# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0003_auto_20160409_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='nickname',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='openid',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\xbe\xae\xe4\xbf\xa1openid', blank=True),
            preserve_default=True,
        ),
    ]
