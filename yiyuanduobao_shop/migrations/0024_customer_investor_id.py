# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0023_address_is_default_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='investor_id',
            field=models.IntegerField(default=-1, null=True, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe4\xba\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7ID', blank=True),
            preserve_default=True,
        ),
    ]
