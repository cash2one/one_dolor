# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0026_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_desc', models.CharField(default=b'', max_length=255, verbose_name='\u72b6\u6001\u8bf4\u660e')),
            ],
            options={
                'verbose_name': '\u4ea4\u6613\u72b6\u6001',
                'verbose_name_plural': '\u4ea4\u6613\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\xa4\xe6\x98\x93\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_status',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\xa4\xe6\x98\x93\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='yiyuanduobao_shop.TransactionStatus', null=True),
            preserve_default=True,
        ),
    ]
