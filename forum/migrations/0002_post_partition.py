# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='partition',
            field=models.CharField(choices=[('Chat', 'Chat'), ('Announcement', 'Announcement'), ('Transaction', 'Transaction'), ('Activity', 'Activity')], default='Chat', max_length=50),
        ),
    ]
