# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0005_auto_20160410_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantBannerImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0')),
                ('img_link', models.ImageField(upload_to=b'imgs/', verbose_name='\u5546\u54c1\u8f6e\u64ad\u56fe\u7247')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_img',
            field=models.ManyToManyField(to='yiyuanduobao_shop.MerchantBannerImg', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchanttype',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
    ]
