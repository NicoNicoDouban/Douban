# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20180329_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default='user', max_length=20, null=True, unique=True, verbose_name='用户名'),
        ),
    ]