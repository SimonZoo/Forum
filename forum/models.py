# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime
# Create your models here.

def time_generator():
    today = datetime.date.today()

class Post(models.Model):
    PARTITION = (
        ('Chat', 'Chat'),
        ('Announcement', 'Announcement'),
        ('Transaction', 'Transaction'),
        ('Activity', 'Activity'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    partition = models.CharField(max_length=50, choices=PARTITION,default='Chat')
    # owner : Current User
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


