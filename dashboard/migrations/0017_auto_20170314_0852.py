# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-14 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20170309_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='archived',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('blocked', 'Blocked'), ('Client Review', 'Client Review')], max_length=20),
        ),
    ]
