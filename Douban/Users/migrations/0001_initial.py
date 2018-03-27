# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 12:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='一篇文章', max_length=20, verbose_name='标题')),
                ('pub_time', models.DateTimeField(verbose_name='发表时间')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击数')),
                ('text', models.TextField(default='', verbose_name='文章内容')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数')),
            ],
            options={
                'verbose_name': '文章信息',
                'verbose_name_plural': '文章信息',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='图书名')),
                ('writer', models.CharField(default='', max_length=50, verbose_name='作者名')),
                ('publisher', models.CharField(default='', max_length=30, verbose_name='出版社')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数')),
            ],
            options={
                'verbose_name': '图书信息',
                'verbose_name_plural': '图书信息',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_time', models.DateTimeField(verbose_name='发表时间')),
                ('text', models.TextField(default='', verbose_name='评论内容')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Books', verbose_name='图书')),
            ],
            options={
                'verbose_name': '评论信息',
                'verbose_name_plural': '评论信息',
            },
        ),
        migrations.CreateModel(
            name='FollowLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '用户关注关联信息',
                'verbose_name_plural': '用户关注关联信息',
            },
        ),
        migrations.CreateModel(
            name='GoodLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateTimeField(verbose_name='点赞时间')),
                ('bookId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Books', verbose_name='图书')),
            ],
            options={
                'verbose_name': '图书点赞关联信息',
                'verbose_name_plural': '图书点赞关联信息',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nick_name', models.CharField(default='小豆瓣儿', max_length=20, verbose_name='昵称')),
                ('password', models.CharField(default='123456', max_length=20, verbose_name='密码')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='邮箱')),
                ('birthday', models.DateTimeField(default='', verbose_name='生日')),
                ('gender', models.CharField(default='保密', max_length=2, verbose_name='性别')),
                ('follow_num', models.IntegerField(default=0, verbose_name='关注数')),
                ('pub_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
                ('address', models.CharField(default='保密', max_length=100, verbose_name='用户地址')),
                ('image', models.CharField(default='image/default.png', max_length=100, verbose_name='用户头像')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='goodlink',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users', verbose_name='点赞的人'),
        ),
        migrations.AddField(
            model_name='followlink',
            name='toId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='被关注者', to='Users.Users', verbose_name='被关注的人'),
        ),
        migrations.AddField(
            model_name='followlink',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='关注者', to='Users.Users', verbose_name='发起关注的人'),
        ),
        migrations.AddField(
            model_name='comments',
            name='commenter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users', verbose_name='发表评论的人'),
        ),
        migrations.AddField(
            model_name='articles',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users', verbose_name='文章作者'),
        ),
    ]
