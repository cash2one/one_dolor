# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0021_auto_20160412_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddrInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.IntegerField(default=0, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80\xe7\xa0\x81')),
                ('addr', models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
