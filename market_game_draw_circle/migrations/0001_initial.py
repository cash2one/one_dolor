# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(default=b'', max_length=255, null=True, verbose_name=b'\xe5\xbe\xae\xe4\xbf\xa1openid', blank=True)),
                ('playtimes', models.IntegerField(default=3, null=True, verbose_name=b'\xe5\x8f\xaf\xe4\xbb\xa5\xe7\x8e\xa9\xe7\x9a\x84\xe6\xac\xa1\xe6\x95\xb0', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
