# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(blank=True, to='post.Post', verbose_name='좋아요 누른 포스트 목록'),
        ),
    ]
