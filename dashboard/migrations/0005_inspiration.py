# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20170214_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspiration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.FileField(upload_to='inspiration/%Y/%m/%d')),
            ],
        ),
    ]
