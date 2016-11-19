# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0018_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='headimg',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f', blank=True),
            preserve_default=True,
        ),
    ]
