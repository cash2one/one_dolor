# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0010_auto_20160411_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerTakePartItemInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('take_part_times', models.IntegerField(default=0, verbose_name=b'\xe5\x8f\x82\xe4\xb8\x8e\xe6\xac\xa1\xe6\x95\xb0')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to='yiyuanduobao_shop.Merchant')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u7528\u6237\u53c2\u4e0e\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u53c2\u4e0e\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-create_time'], 'verbose_name': '\u7528\u6237', 'verbose_name_plural': '\u7528\u6237'},
        ),
        migrations.AddField(
            model_name='item',
            name='customer_take_part_info',
            field=models.ManyToManyField(to='yiyuanduobao_shop.CustomerTakePartItemInfo', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x8f\x82\xe4\xb8\x8e\xe4\xbf\xa1\xe6\x81\xaf'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d', blank=True),
            preserve_default=True,
        ),
    ]
