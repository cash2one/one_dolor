# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0017_auto_20160411_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe8\xb4\xa6\xe6\x88\xb7\xe5\x90\x8d'),
            preserve_default=True,
        ),
    ]
