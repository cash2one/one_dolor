# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0007_auto_20160410_2254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchant',
            options={'ordering': ['-create_time'], 'verbose_name': '\u5546\u54c1', 'verbose_name_plural': '\u5546\u54c1'},
        ),
        migrations.AlterModelOptions(
            name='merchantbannerimg',
            options={'ordering': ['-create_time'], 'verbose_name': '\u5546\u54c1\u8f6e\u64ad\u56fe\u7247', 'verbose_name_plural': '\u5546\u54c1\u8f6e\u64ad\u56fe\u7247'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['-create_time'], 'verbose_name': '\u4e00\u5143\u593a\u5b9d\u5546\u5e97', 'verbose_name_plural': '\u4e00\u5143\u593a\u5b9d\u5546\u5e97'},
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='price_unit',
        ),
        migrations.AddField(
            model_name='merchant',
            name='price',
            field=models.IntegerField(default=1, verbose_name='\u5546\u54c1\u4ef7\u683c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
    ]
