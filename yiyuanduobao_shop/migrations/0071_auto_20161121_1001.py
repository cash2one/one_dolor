# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0070_shop_qrcode_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_type_desc', models.CharField(default=b'', max_length=255, verbose_name='\u4ea4\u6613\u65b9\u5f0f')),
            ],
            options={
                'verbose_name': '\u4ea4\u6613\u65b9\u5f0f',
                'verbose_name_plural': '\u4ea4\u6613\u65b9\u5f0f',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\xa4\xe6\x98\x93\xe6\x96\xb9\xe5\xbc\x8f', blank=True, to='yiyuanduobao_shop.TransactionType', null=True),
            preserve_default=True,
        ),
    ]
