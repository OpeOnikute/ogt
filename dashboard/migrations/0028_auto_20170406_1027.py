# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-06 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_sentemailslog_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentemailslog',
            name='content',
            field=models.TextField(default='Test content', max_length=500),
        ),
        migrations.AddField(
            model_name='sentemailslog',
            name='subject',
            field=models.CharField(default='Test message', max_length=100),
        ),
    ]
