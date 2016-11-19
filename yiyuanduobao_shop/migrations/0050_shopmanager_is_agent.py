# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0049_auto_20160503_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopmanager',
            name='is_agent',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u4ee3\u7406\u5546'),
            preserve_default=True,
        ),
    ]
