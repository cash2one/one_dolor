# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0004_auto_20160409_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='mer_type',
            field=models.ForeignKey(verbose_name='\u5546\u54c1\u7c7b\u578b', to='yiyuanduobao_shop.MerchantType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='shop',
            field=models.ForeignKey(related_name='shop_merchant', verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x95\x86\xe5\xba\x97', to='yiyuanduobao_shop.Shop'),
            preserve_default=True,
        ),
    ]
