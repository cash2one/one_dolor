# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0044_auto_20160430_1222'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-create_time'], 'verbose_name': '\u9879\u76ee', 'verbose_name_plural': '\u9879\u76ee'},
        ),
        migrations.AddField(
            model_name='merchant',
            name='auto_up_shelve',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u81ea\u52a8\u4e0a\u67b6'),
            preserve_default=True,
        ),
    ]
