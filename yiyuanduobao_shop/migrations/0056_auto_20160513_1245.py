# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0055_auto_20160513_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='lottery_time',
            field=models.DateTimeField(null=True, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe4\xb8\xad\xe5\xa5\x96\xe6\x97\xb6\xe9\x97\xb4', blank=True),
            preserve_default=True,
        ),
    ]
