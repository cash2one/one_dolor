# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0022_addrinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default_addr',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u4e3a\u9ed8\u8ba4\u5730\u5740'),
            preserve_default=True,
        ),
    ]
