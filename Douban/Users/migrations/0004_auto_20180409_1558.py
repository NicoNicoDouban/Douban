# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-09 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_books_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='src',
            field=models.ImageField(default='/media/book_image/defalut', upload_to='media/pictures/', verbose_name='封面url地址'),
        ),
    ]
