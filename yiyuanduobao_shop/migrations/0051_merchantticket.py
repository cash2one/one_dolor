# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0050_shopmanager_is_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_index', models.IntegerField(default=0, verbose_name=b'\xe4\xb8\x8b\xe6\xa0\x87')),
                ('ticket_no', models.IntegerField(default=0, verbose_name=b'\xe5\x8f\xb7\xe7\xa0\x81')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
