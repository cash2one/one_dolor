# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0032_auto_20160419_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_no', models.CharField(default=b'', max_length=255, verbose_name='\u53c2\u4e0e\u53f7\u7801')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('order', models.ForeignKey(verbose_name='\u5bf9\u5e94\u8ba2\u5355', to='yiyuanduobao_shop.Order')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u53c2\u4e0e\u53f7\u7801',
                'verbose_name_plural': '\u53c2\u4e0e\u53f7\u7801',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
    ]
