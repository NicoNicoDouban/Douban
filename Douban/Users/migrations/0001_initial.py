# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-03 00:09
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_remove_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='一篇文章', max_length=20, verbose_name='标题')),
                ('pub_time', models.DateTimeField(default=datetime.datetime(2018, 4, 3, 8, 9, 11, 694385), verbose_name='发表时间')),
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
                ('author', models.CharField(default='', max_length=50, verbose_name='作者名')),
                ('publisher', models.CharField(default='', max_length=30, verbose_name='出版社')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数')),
                ('text', models.TextField(default='暂无介绍', verbose_name='简介')),
                ('src', models.CharField(default='image/default.png', max_length=100, verbose_name='封面url地址')),
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
            name='userActive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_code', models.CharField(max_length=30, verbose_name='激活码')),
                ('status', models.CharField(default='r', max_length=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '用户激活验证码',
                'verbose_name_plural': '用户激活验证码',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(default='', max_length=254, unique=True, verbose_name='邮箱')),
                ('birthday', models.DateField(default='2000-01-01', verbose_name='生日')),
                ('gender', models.CharField(choices=[('F', '女'), ('M', '男'), ('S', '保密')], default='S', max_length=1, verbose_name='性别')),
                ('follow_num', models.IntegerField(default=0, verbose_name='被关注数')),
                ('pub_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
                ('address', models.CharField(default='保密', max_length=100, verbose_name='用户地址')),
                ('image', models.CharField(default='image/default.png', max_length=100, verbose_name='用户头像')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='useractive',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='goodlink',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AddField(
            model_name='followlink',
            name='toId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='被关注者', to=settings.AUTH_USER_MODEL, verbose_name='被关注者'),
        ),
        migrations.AddField(
            model_name='followlink',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='关注者', to=settings.AUTH_USER_MODEL, verbose_name='关注者'),
        ),
        migrations.AddField(
            model_name='comments',
            name='commenter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='文章作者'),
        ),
    ]
