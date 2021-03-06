# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-08 09:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0028_auto_20170406_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='Test message', max_length=100)),
                ('content', models.TextField(default='Test content', max_length=500)),
                ('attachments', models.CharField(choices=[('No', 'NO'), ('Yes', 'YES')], max_length=5)),
                ('attachment_type', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sentemailslog',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
