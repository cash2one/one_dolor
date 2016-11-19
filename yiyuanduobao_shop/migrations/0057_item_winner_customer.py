# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0056_auto_20160513_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='winner_customer',
            field=models.ForeignKey(related_name='item_winner_customer', verbose_name=b'\xe4\xb8\xad\xe5\xa5\x96\xe5\xae\xa2\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Customer', null=True),
            preserve_default=True,
        ),
    ]
