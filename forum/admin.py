# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Comment
import sys
# Register your models here.


reload(sys)
sys.setdefaultencoding('utf-8')
admin.site.register(Post)
admin.site.register(Comment)