# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0038_customer_last_login_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u9879\u76ee\u7c7b\u578b')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='proxy_sale_customer',
            field=models.ForeignKey(verbose_name=b'\xe4\xbb\xa3\xe9\x94\x80\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Customer', null=True),
            preserve_default=True,
        ),
    ]
