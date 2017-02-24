# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-16 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170216_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='completion_status',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]