# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20171028_0218'),
        ('member', '0002_auto_20171028_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
        migrations.AddField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(to='post.Post', verbose_name='좋아요 누른 포스트 목록'),
        ),
    ]