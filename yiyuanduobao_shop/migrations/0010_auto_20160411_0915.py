# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0009_auto_20160410_2344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-create_time'], 'verbose_name': '\u5546\u54c1\u671f', 'verbose_name_plural': '\u5546\u54c1\u671f'},
        ),
        migrations.AddField(
            model_name='item',
            name='take_part_num',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xb2\xe5\x8f\x82\xe4\xb8\x8e\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0'),
            preserve_default=True,
        ),
    ]
