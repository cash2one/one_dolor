# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='progress',
            field=models.FloatField(default=0.0, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe8\xbf\x9b\xe5\xba\xa6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='order_times',
            field=models.IntegerField(default=1, verbose_name='\u53c2\u4e0e\u6b21\u6570'),
            preserve_default=True,
        ),
    ]
