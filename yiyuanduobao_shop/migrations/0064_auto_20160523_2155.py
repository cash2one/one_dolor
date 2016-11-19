# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0063_auto_20160516_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='auto_up_shelve',
            field=models.BooleanField(default=True, verbose_name='\u672c\u671f\u7ed3\u675f\uff0c\u662f\u5426\u81ea\u52a8\u4e0a\u67b6'),
            preserve_default=True,
        ),
    ]
