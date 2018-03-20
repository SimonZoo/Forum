# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.login, name='logout'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^post_create/$', views.PostCreate.as_view(), name='post_create'),
    url(r'^comment_create/$', views.CommentCreate.as_view(), name='comment_create'),
    url(r'^post/(?P<pid>\d+)/$', views.post_detail, name='post_detail'),
]