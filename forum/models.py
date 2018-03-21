# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Post(models.Model):
    PARTITION = (
        ('Chat', 'Chat'),
        ('Announcement', 'Announcement'),
        ('Transaction', 'Transaction'),
        ('Activity', 'Activity'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    partition = models.CharField(max_length=50, choices=PARTITION, default='Chat')
    owner = models.CharField(max_length=100, default='User')
    content = models.CharField(max_length=1000, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, default='New Comment')
    time = models.DateTimeField(default=timezone.now)
    owner = models.CharField(max_length=100, default='User')

    def __str__(self):
        return str(self.id)