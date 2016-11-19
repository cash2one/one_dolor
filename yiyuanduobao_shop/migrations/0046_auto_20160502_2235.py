# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0045_auto_20160430_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeMsg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\xb6\x88\xe6\x81\xaftitle')),
                ('context', models.CharField(default=b'', max_length=3000, verbose_name=b'\xe6\xb6\x88\xe6\x81\xaf\xe5\x86\x85\xe5\xae\xb9')),
                ('customer', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='yiyuanduobao_shop.Customer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeMsgStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_name', models.CharField(default=b'', max_length=255, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='noticemsg',
            name='notice_msg_status',
            field=models.ForeignKey(verbose_name=b'\xe6\xb6\x88\xe6\x81\xaf\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='yiyuanduobao_shop.NoticeMsgStatus', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x95\x86\xe5\xba\x97\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
    ]
