# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0008_auto_20160410_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u72b6\u6001\u540d\u79f0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='item',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='item_status',
            field=models.ForeignKey(verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe7\x8a\xb6\xe6\x80\x81', to='yiyuanduobao_shop.ItemStatus'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='merchant',
            field=models.ForeignKey(related_name='merchant_item', verbose_name=b'\xe5\x95\x86\xe5\x93\x81', to='yiyuanduobao_shop.Merchant'),
            preserve_default=True,
        ),
    ]
