# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0029_item_take_part_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_no', models.CharField(default=b'', max_length=255, verbose_name='\u5f69\u7968\u671f\u53f7')),
                ('result', models.CharField(default=b'', max_length=255, verbose_name='\u5f00\u5956\u7ed3\u679c')),
            ],
            options={
                'verbose_name': '\u65f6\u65f6\u5f69',
                'verbose_name_plural': '\u65f6\u65f6\u5f69',
            },
            bases=(models.Model,),
        ),
    ]
