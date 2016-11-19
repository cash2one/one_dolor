# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0035_auto_20160419_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopmanager',
            options={'ordering': ['-create_time'], 'verbose_name': '\u593a\u5b9d\u5e97\u7ba1\u7406\u5458', 'verbose_name_plural': '\u593a\u5b9d\u5e97\u7ba1\u7406\u5458'},
        ),
        migrations.AddField(
            model_name='shop',
            name='contract_mobile',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe7\x94\xb5\xe8\xaf\x9d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='contract_name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe5\xa7\x93\xe5\x90\x8d'),
            preserve_default=True,
        ),
    ]
