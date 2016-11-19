# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0011_auto_20160411_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customertakepartiteminfo',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='item',
            name='customer_take_part_info',
        ),
        migrations.DeleteModel(
            name='CustomerTakePartItemInfo',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(verbose_name='\u8ba2\u5355\u72b6\u6001', to='yiyuanduobao_shop.OrderStatus'),
            preserve_default=True,
        ),
    ]
