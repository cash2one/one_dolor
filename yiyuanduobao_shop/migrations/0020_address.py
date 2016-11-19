# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0019_customer_headimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\x94\xb6\xe4\xbb\xb6\xe4\xba\xba\xe5\xa7\x93\xe5\x90\x8d')),
                ('province', models.CharField(default=b'', max_length=255, verbose_name=b'\xe7\x9c\x81')),
                ('city', models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\xb8\x82')),
                ('district', models.CharField(default=b'', max_length=255, verbose_name=b'\xe5\x8c\xba')),
                ('detail_address', models.CharField(default=b'', max_length=255, verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe5\x9c\xb0\xe5\x9d\x80')),
                ('postcode', models.CharField(default=b'', max_length=255, verbose_name=b'\xe9\x82\xae\xe7\xbc\x96')),
                ('mobile', models.CharField(default=b'', max_length=255, verbose_name=b'\xe6\x94\xb6\xe4\xbb\xb6\xe4\xba\xba\xe6\x89\x8b\xe6\x9c\xba')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
