# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0025_order_order_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_no', models.IntegerField(default=1, verbose_name=b'\xe4\xba\xa4\xe6\x98\x93\xe7\xbc\x96\xe5\x8f\xb7')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('orders', models.ManyToManyField(to='yiyuanduobao_shop.Order', null=True, verbose_name=b'\xe5\x8c\x85\xe5\x90\xab\xe8\xae\xa2\xe5\x8d\x95', blank=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u4ea4\u6613',
                'verbose_name_plural': '\u4ea4\u6613',
            },
            bases=(models.Model,),
        ),
    ]
