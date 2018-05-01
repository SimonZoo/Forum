from django.contrib import admin

from .models import Post, Comment
# Register your models here.
import sys

reload(sys)
sys.setdefaultencoding('utf8')
admin.site.register(Post)
admin.site.register(Comment)
