# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0012_auto_20160411_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance_coins', models.IntegerField(default=0, verbose_name=b'\xe5\xa4\xba\xe5\xae\x9d\xe5\xb8\x81\xe4\xbd\x99\xe9\xa2\x9d')),
                ('points', models.IntegerField(default=0, verbose_name=b'\xe5\xa4\xba\xe5\xae\x9d\xe7\xa7\xaf\xe5\x88\x86')),
                ('total_recharge', models.IntegerField(default=0, verbose_name=b'\xe6\x80\xbb\xe5\x85\x85\xe5\x80\xbc\xe9\x87\x91\xe9\xa2\x9d')),
                ('balance_redpack', models.IntegerField(default=0, verbose_name=b'\xe5\x8f\xaf\xe9\xa2\x86\xe7\xba\xa2\xe5\x8c\x85\xe9\x87\x91\xe9\xa2\x9d')),
                ('withdraw_redpack', models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xb2\xe9\xa2\x86\xe7\xba\xa2\xe5\x8c\x85\xe9\x87\x91\xe9\xa2\x9d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-create_time'], 'verbose_name': '\u8ba2\u5355', 'verbose_name_plural': '\u8ba2\u5355'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='item',
            name='take_part_num',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(related_name='customer_order', verbose_name=b'\xe5\x8f\x82\xe4\xb8\x8e\xe7\x94\xa8\xe6\x88\xb7', to='yiyuanduobao_shop.Customer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(related_name='item_order', verbose_name=b'\xe5\x8f\x82\xe4\xb8\x8e\xe9\xa1\xb9\xe7\x9b\xae', to='yiyuanduobao_shop.Item'),
            preserve_default=True,
        ),
    ]
