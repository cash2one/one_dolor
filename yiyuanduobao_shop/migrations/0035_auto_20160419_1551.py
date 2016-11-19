# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yiyuanduobao_shop', '0034_lotteryticket_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe6\x9c\xac\xe6\x9c\x9f\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lotteryresult',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='merchant',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
    ]
