# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-29 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20180325_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, default='your nickname', max_length=20, null=True),
        ),
    ]