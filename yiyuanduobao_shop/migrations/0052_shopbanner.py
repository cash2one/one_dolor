# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0051_merchantticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_img', models.ImageField(upload_to=b'imgs/', verbose_name='\u9996\u9875banner\u56fe')),
                ('banner_link', models.CharField(default=b'#', max_length=255, null=True, verbose_name='banner\u94fe\u63a5\u5730\u5740', blank=True)),
            ],
            options={
                'verbose_name': '\u9996\u9875\u8f6e\u64ad\u56fe',
                'verbose_name_plural': '\u9996\u9875\u8f6e\u64ad\u56fe',
            },
            bases=(models.Model,),
        ),
    ]
