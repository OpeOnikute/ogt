# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-16 09:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20170216_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='start_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2017, 2, 16, 9, 15, 19, 159000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]